"""Module to analyze stackoverflow"""
from xml.etree import ElementTree
import re
from collections import Counter
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging

APPLICATION_NAME = "stackoverflow_analytics"
DATASET_DEFAULT_ENCODING = "utf-8"
STOPWORDS_DEFAULT_ENCODING = "koi8-r"

logger = logging.getLogger(APPLICATION_NAME)


class NoStopWordsError(Exception):
    """Exception throws when list if stopwords is empty"""


class StackoverflowAnalyzer:
    """Stackoverflow analyzer"""
    REQUIRED_ATTRIBS = ("PostTypeId", "CreationDate", "Score", "Title")

    def __init__(self) -> None:
        self.content = None
        self.scores = None
        self.stopwords = None

    @classmethod
    def read_xml(
            cls, filepath: str, encoding: str = DATASET_DEFAULT_ENCODING,
            check_attrib_values: dict = None
    ):
        """Read xml from file"""
        azr = StackoverflowAnalyzer()
        content = []
        with open(filepath, encoding=encoding) as fin:
            for line in fin.readlines():
                try:
                    et = ElementTree.fromstring(line)
                except ElementTree.ParseError:
                    continue
                if not all(attr in et.attrib for attr in cls.REQUIRED_ATTRIBS):
                    continue
                good_info = True
                if check_attrib_values is not None:
                    for k, v in check_attrib_values.items():
                        if k in et.attrib:
                            if et.attrib.get(k) != v:
                                good_info = False
                                break
                if good_info:
                    info = {
                        "year": int(et.attrib["CreationDate"][:4]),
                        "score": int(et.attrib["Score"]),
                        "title_words": set(re.findall(r"\w+", et.attrib["Title"].lower()))
                    }
                    content.append(info)

        azr.content = content
        logger.info("process XML dataset, ready to serve queries")
        return azr

    def load_stopwords(self, filepath: str, encoding: str = STOPWORDS_DEFAULT_ENCODING) -> None:
        """Load stopwords from file"""
        with open(filepath, encoding=encoding) as fin:
            self.stopwords = fin.read().split()

    def analyze(
            self, top_n: int, *, year_from: int, year_to: int,
            check_stopwords: bool = False
    ) -> None:
        """Analyze questions"""
        if check_stopwords and not self.stopwords:
            raise NoStopWordsError
        res = {
            "start": year_from,
            "end": year_to,
            "top": []
        }
        if self.content:
            post_scores = [
                (c["title_words"], c["score"])
                for c in self.content
                if year_from <= c["year"] <= year_to
            ]

            scores = Counter()
            for ps in post_scores:
                words, score = ps
                for word in words:
                    if check_stopwords:
                        if word in self.stopwords:
                            continue
                    scores[word] += score
            if len(scores) < top_n:
                logger.warning(
                    'not enough data to answer, found %s words out of %s for period "%s,%s"',
                    len(scores), top_n, year_from, year_to
                )
            top = sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:top_n]
            res["top"] = [list(t) for t in top]
        print(json.dumps(res))


def setup_logging():
    """Setup logging"""
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="%(levelname)s: %(message)s"
    )

    debug_file_handler = logging.FileHandler(
        filename="stackoverflow_analytics.log"
    )
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)

    warn_file_handler = logging.FileHandler(
        filename="stackoverflow_analytics.warn"
    )
    warn_file_handler.setLevel(logging.WARNING)
    warn_file_handler.setFormatter(formatter)

    logger.addHandler(debug_file_handler)
    logger.addHandler(warn_file_handler)


def callback_analyze(arguments: "NameSpace") -> None:
    """Callback"""
    azr = StackoverflowAnalyzer.read_xml(
        arguments.questions,
        check_attrib_values={"PostTypeId": "1"}
    )
    azr.load_stopwords(arguments.stop_words)
    with open(arguments.queries) as fin:
        for line in fin.readlines():
            year_from, year_to, top_n = map(int, line.split(","))
            logger.debug('got query "%s,%s,%s"', year_from, year_to, top_n)
            azr.analyze(top_n, year_from=year_from, year_to=year_to, check_stopwords=True)
    logger.info("finish processing queries")


def setup_parser(parser: "ArgumentParser") -> None:
    """Setup parser"""
    parser.add_argument(
        "--questions",
        required=True,
        help="path to questions"
    )
    parser.add_argument(
        "--stop-words",
        required=True,
        help="path to stop words"
    )
    parser.add_argument(
        "--queries",
        required=True,
        help="path to queries"
    )
    parser.set_defaults(callback=callback_analyze)


def main() -> None:
    """Process arguments and analyze"""
    setup_logging()
    parser = ArgumentParser(
        prog="stackoverflow analyzer",
        description="tool to find the most popular words for a period of time",
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
