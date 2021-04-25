from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import pickle


class AsadovParser:
    ROOT_URL = "http://asadove.ru/stihi/"

    def __init__(self):
        self.poems = []
        self.urls = self._get_urls()

    @staticmethod
    def _soup_url(url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        return soup

    @staticmethod
    def _remove_tags(text):
        text = re.sub(r"\<[^>]*\>", "", text)
        return text

    def _get_text_from_url(self, url):
        soup = self._soup_url(url)
        text_with_tags = "\n".join(map(str, soup.find_all("p")))
        text = self._remove_tags(text_with_tags)
        return text_with_tags

    def _get_urls(self):
        soup = self._soup_url(self.ROOT_URL)
        urls = []
        for a in soup.find_all("a", {"rel": "bookmark"}, href=True):
            urls.append(a["href"])
        return urls

    def parse(self):
        for url in tqdm(self.urls):
            text = self._get_text_from_url(url)
            poems = text.split(r"<p>")
            for poem in poems:
                poem = self._remove_tags(poem)
                if poem:
                    self.poems.append(poem)

    def save(self, fname):
        with open(fname, mode="wb") as fp:
            pickle.dump(self.poems, fp)


def main():
    ap = AsadovParser()
    ap.parse()
    ap.save("asadov.pkl")


if __name__ == "__main__":
    main()
