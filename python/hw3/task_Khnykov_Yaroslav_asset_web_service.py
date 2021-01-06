"""Asset web service"""
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)
CBR_BASE_URL = "https://www.cbr.ru/eng/"
CBR_KEY_INDICATORS = f"{CBR_BASE_URL}/key-indicators/"
CBR_DAILY_EXCHANGE_RATES = f"{CBR_BASE_URL}/currency_base/daily/"


def convert_float(text):
    """Convert text to float"""
    float_ = float(text.replace(",", ""))
    return float_


def parse_raw_items(soup, mode):
    """Parse raw items"""
    if mode == "currency":
        names_td_class = "value td-w-13 _inner"
        value_slice = slice(1, None, 2)
    elif mode == "precious_metals":
        names_td_class = "value td-w-9 _inner"
        value_slice = slice(None)
    else:
        raise NotImplementedError

    collection = {}
    raw_names = soup.find_all("td", class_=names_td_class)
    names = [rn.find("div", class_="col-md-3 offset-md-1 _subinfo").text for rn in raw_names]
    raw_values = soup.find_all("td", class_=re.compile(r"value td-w-4 _bold _end mono-num.*"))
    values = [convert_float(raw_value.text) for raw_value in raw_values][value_slice]
    for n, v in zip(names, values):
        collection[n] = v

    return collection


def parse_cbr_key_indicators(raw_html):
    """Parse CBR key indicators"""
    soup = BeautifulSoup(raw_html, "lxml")
    raw_currency, raw_precious_metals = soup.find_all(
        "div", class_="table key-indicator_table", limit=2
    )
    indicator_collection = {
        **parse_raw_items(raw_currency, mode="currency"),
        **parse_raw_items(raw_precious_metals, mode="precious_metals")
    }
    return indicator_collection


def parse_cbr_currency_base_daily(raw_html):
    """Parse CBR currency daily rates"""
    soup = BeautifulSoup(raw_html, "lxml")
    table = soup.find("table", class_="data")
    _headers, *rows = table.find_all("tr")
    collection = {}
    for r in rows:
        _raw_num_code, raw_char_code, raw_unit, _raw_currency, raw_rate = r.find_all("td")
        collection[raw_char_code.text] = convert_float(raw_rate.text) / convert_float(raw_unit.text)
    return collection


@app.errorhandler(404)
def page_is_not_found(_error):
    """Page is not found"""
    return "This route is not found", 404


@app.errorhandler(Exception)
def page_is_unavailable(_error):
    """Page is unavailable"""
    return "CBR service is unavailable", 503


@app.route("/cbr/daily")
def get_daily_data():
    """Get daily data"""
    response = requests.get(CBR_DAILY_EXCHANGE_RATES)
    res = parse_cbr_currency_base_daily(response.text)
    return jsonify(res)


@app.route("/cbr/key_indicators")
def get_key_indicators_data():
    """Get key indicators data"""
    response = requests.get(CBR_KEY_INDICATORS)
    res = parse_cbr_key_indicators(response.text)
    return jsonify(res)


class Asset:
    """Asset"""
    def __init__(self, char_code, name, capital, interest):
        self.char_code = char_code
        self.name = name
        self.capital = capital
        self.interest = interest

    def list_view(self):
        """List view"""
        list_view_ = [self.char_code, self.name, self.capital, self.interest]
        return list_view_

    def calculate_revenue(self, years, rate):
        """Calculate revenue"""
        revenue = self.capital * ((1.0 + self.interest) ** years - 1.0)
        revenue *= rate
        return revenue


class Bank:
    """Bank"""
    def __init__(self):
        self.names = []
        self.asset_collection = []

    def add(self, char_code, name, capital, interest):
        """Add"""
        asset = Asset(char_code, name, capital, interest)
        self.asset_collection.append(asset)
        self.names.append(name)

    def __contains__(self, name):
        return name in self.names

    def __iter__(self):
        return iter(self.asset_collection)

    def list_view(self):
        """List view"""
        return sorted([asset.list_view() for asset in self.asset_collection])

    def clear(self):
        """Clear"""
        self.names.clear()
        self.asset_collection.clear()

    def get_by_name(self, *names):
        """Get by name"""
        info = sorted([
            self.asset_collection[i].list_view()
            for i, name in enumerate(self.names)
            if name in names
        ])
        return info


app.bank = Bank()


@app.route("/api/asset/add/<char_code>/<name>/<capital>/<interest>")
def add_asset(char_code, name, capital, interest):
    """Add asset"""
    capital = float(capital)
    interest = float(interest)
    if name in app.bank:
        return "", 403
    app.bank.add(char_code, name, capital, interest)
    return f"Asset {name} was successfully added", 200


@app.route("/api/asset/list")
def show_assets():
    """Show assets"""
    list_view_ = app.bank.list_view()
    return jsonify(list_view_), 200


@app.route("/api/asset/cleanup")
def cleanup_assets():
    """Cleanup assets"""
    app.bank.clear()
    return "", 200


@app.route("/api/asset/get")
def get_info():
    """Get info"""
    names = request.args.getlist("name")
    info = app.bank.get_by_name(*names)
    return jsonify(info), 200


@app.route("/api/asset/calculate_revenue")
def get_revenue():
    """Get revenue"""
    revenue_collection = {}
    periods = [int(p) for p in request.args.getlist("period")]
    for period in periods:
        total_revenue = 0.0
        for asset in app.bank:
            if asset.char_code == "RUB":
                rate = 1
            elif (
                asset.char_code in ("USD", "EUR")
                or asset.char_code != asset.char_code.upper()
            ):
                rate = get_key_indicators_data().get_json().get(asset.char_code, 0)
            else:
                rate = get_daily_data().get_json().get(asset.char_code, 0)
            total_revenue += asset.calculate_revenue(period, rate)
        revenue_collection[period] = total_revenue
    return jsonify(revenue_collection), 200


if __name__ == "__main__":
    app.run(debug=True)