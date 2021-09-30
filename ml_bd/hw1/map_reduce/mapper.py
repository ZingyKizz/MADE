import sys
import numpy as np
from typing import NoReturn, Optional, List

from const import PRICES_OUTPUT_PATH, DEFAULT_ENCODING, DEFAULT_SEPARATOR


class Mapper:
    """Класс маппера"""

    DEFAULT_CHUNK_SIZE = 1000

    def __init__(
        self,
        file_path: str,
        encoding: str = DEFAULT_ENCODING,
        chunk_size: Optional[int] = None,
    ) -> NoReturn:
        self.file_path = file_path
        self.encoding = encoding
        self.chunk_size = chunk_size or self.DEFAULT_CHUNK_SIZE

    @staticmethod
    def _chunk_statistics(chunk: List[float]) -> NoReturn:
        """Подсчет статистик в текущем chunk"""
        size = len(chunk)
        mean = np.mean(chunk)
        variance = np.var(chunk)
        sys.stdout.write(f"{size} {mean} {variance}{DEFAULT_SEPARATOR}")

    def run(self) -> NoReturn:
        """Запуск"""
        cur_chunk_size = 0
        cur_chunk = []
        with open(self.file_path, encoding=self.encoding, mode="r") as f:
            for line in f:
                price = float(line.rstrip())
                cur_chunk.append(price)
                cur_chunk_size += 1
                if cur_chunk_size == self.chunk_size:
                    self._chunk_statistics(cur_chunk)
                    cur_chunk.clear()
                    cur_chunk_size = 0
            if cur_chunk_size:
                self._chunk_statistics(cur_chunk)


def main() -> NoReturn:
    """Основная программа"""
    mapper = Mapper(PRICES_OUTPUT_PATH)
    mapper.run()


if __name__ == "__main__":
    main()
