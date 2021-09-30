import sys
from typing import NoReturn

from const import RESULT_OUTPUT_PATH, DEFAULT_ENCODING


class Reducer:
    """Класс редьюсера"""

    def __init__(self, result_output_path: str, encoding: str = DEFAULT_ENCODING) -> None:
        self.result_output_path = result_output_path
        self.encoding = encoding

    def run(self) -> NoReturn:
        cur_size = 0
        cur_mean = None
        cur_variance = None

        for line in sys.stdin:
            chunk_size, chunk_mean, chunk_variance = map(float, line.split())

            if not cur_size:
                cur_size, cur_mean, cur_variance = chunk_size, chunk_mean, chunk_variance
                continue

            cur_variance = cur_size * cur_variance + chunk_size * chunk_variance
            cur_variance /= cur_size + chunk_size
            cur_variance += (
                    cur_size
                    * chunk_size
                    * ((cur_mean - chunk_mean) / (cur_size + chunk_size)) ** 2
            )

            cur_mean = cur_size * cur_mean + chunk_size * chunk_mean
            cur_mean /= cur_size + chunk_size

            cur_size += chunk_size

        with open(self.result_output_path, encoding=self.encoding, mode="a") as f:
            f.write(f"MapReduce Mean: {cur_mean}, MapReduce Variance: {cur_variance}")


def main() -> NoReturn:
    """Основная программа"""
    reducer = Reducer(RESULT_OUTPUT_PATH)
    reducer.run()


if __name__ == "__main__":
    main()
