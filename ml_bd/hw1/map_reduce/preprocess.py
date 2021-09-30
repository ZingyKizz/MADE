import pandas as pd
import numpy as np
from typing import NoReturn

from const import (
    DATA_INPUT_PATH,
    PRICE_COLNAME,
    DEFAULT_ENCODING,
    DEFAULT_SEPARATOR,
    PRICES_OUTPUT_PATH,
    RESULT_OUTPUT_PATH,
)


def extract_prices(data_input_path: str) -> np.ndarray:
    """Извлечение цен из сырых данных в виде numpy массива"""
    prices = pd.read_csv(data_input_path)[PRICE_COLNAME].values
    return prices


def write_prices(
    prices: np.ndarray,
    prices_output_path: str,
    encoding: str = DEFAULT_ENCODING,
    sep: str = DEFAULT_SEPARATOR,
) -> NoReturn:
    """Запись цен в файл"""
    with open(prices_output_path, encoding=encoding, mode="w") as f:
        for p in prices:
            f.write(f"{p}{sep}")


def write_statistics(
    prices: np.ndarray, result_output_path=RESULT_OUTPUT_PATH, encoding=DEFAULT_ENCODING
) -> NoReturn:
    """Запись статистик в результирующий файл, посчитанных через numpy"""
    mean = np.mean(prices)
    variance = np.var(prices)

    with open(result_output_path, encoding=encoding, mode="w") as f:
        f.write(f"Numpy Mean: {mean}, Numpy Variance: {variance}")


def main() -> NoReturn:
    """Основная программа"""
    prices = extract_prices(DATA_INPUT_PATH)
    write_prices(prices, PRICES_OUTPUT_PATH)
    write_statistics(prices, RESULT_OUTPUT_PATH)


if __name__ == "__main__":
    main()
