"""This module does blah blah."""

import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
from io import TextIOWrapper
from collections import defaultdict
from functools import reduce
import struct
import sys


DEFAULT_DATASET_PATH = "wikipedia_sample.txt"
DEFAULT_INVERTED_INDEX_STORE_PATH = "inverted_index.bin"


class EncodedFileType(FileType):
    """EncodedFileType"""
    def __call__(self, string):
        if string == "-":
            if "r" in self._mode:
                stdin = TextIOWrapper(sys.stdin.buffer, encoding=self._encoding)
                return stdin
            if "w" in self._mode:
                stdout = TextIOWrapper(sys.stdout.buffer, encoding=self._encoding)
                return stdout
            msg = "argument '-' with mode %r" % self._mode
            raise ValueError(msg)
        try:
            return open(string, self._mode, self._bufsize, self._encoding,
                        self._errors)
        except OSError as exc:
            args = {"filename": string, "error": exc}
            message = "can't open '%(filename)s': %(error)s"
            raise ArgumentTypeError(message % args)

    def fix(self):
        """fix"""


class StoragePolicy:
    """StoragePolicy"""
    @staticmethod
    def _pack(f, element, c_type):
        if c_type in ("I", "H"):
            binary_element = struct.pack(f">{c_type}", element)
            f.write(binary_element)
        elif c_type == "s":
            encoded_element = element.encode("utf-8")
            f.write(
                struct.pack(">I", len(encoded_element))
            )
            binary_element = struct.pack(f">{len(encoded_element)}s", encoded_element)
            f.write(binary_element)

    @staticmethod
    def dump(filepath, word_to_docs):
        """Dump"""
        fin = open(filepath, mode="wb")
        StoragePolicy._pack(fin, len(word_to_docs.keys()), "I")
        for word, doc_ids in word_to_docs.items():
            StoragePolicy._pack(fin, word, "s")
            ids_count = len(doc_ids)
            StoragePolicy._pack(fin, ids_count, "H")
            for id_ in doc_ids:
                StoragePolicy._pack(fin, int(id_), "I")
        fin.close()

    @staticmethod
    def _unpack(f, c_type):
        """unpack"""
        if c_type == "H":
            binary_element_length = f.read(2)
            element_length = struct.unpack(">H", binary_element_length)[0]
            return element_length
        binary_element_length = f.read(4)
        element_length = struct.unpack(">I", binary_element_length)[0]
        if c_type == "I":
            return element_length
        element_format = f">{element_length}s"
        binary_element = f.read(element_length)
        element = struct.unpack(element_format, binary_element)[0].decode("utf-8")
        return element

    @staticmethod
    def load(filepath):
        """Load"""
        f = open(filepath, mode="rb")
        length = StoragePolicy._unpack(f, "I")
        res = {}
        while length:
            key = StoragePolicy._unpack(f, "s")
            doc_ids_size = StoragePolicy._unpack(f, "H")
            values = set()
            for _ in range(doc_ids_size):
                values.add(str(StoragePolicy._unpack(f, "I")))
            res[key] = values
            length -= 1
        return defaultdict(set, res)


def load_documents(fin):
    """Load documents"""
    documents = {}
    with open(fin, mode="r", encoding="utf-8") as f:
        for row in f:
            identifier, text = row.strip().split(maxsplit=1)
            documents[identifier] = text
    return documents


def build_inverted_index(documents):
    """Build inverted index"""
    index = InvertedIndex()
    word_to_docs = defaultdict(set)
    for doc_id, doc in documents.items():
        for word in doc.split():
            word_to_docs[word].add(doc_id)
    index.word_to_docs = word_to_docs
    index.number_of_words = len(word_to_docs.keys())
    return index


class InvertedIndex:
    """Инвертированный индекс"""
    def __init__(self):
        self.number_of_words = 0
        self.word_to_docs = None

    def __repr__(self):
        return str(self.word_to_docs)

    def query(self, words):
        """query"""
        assert isinstance(words, list)
        word_to_docs = map(lambda k: self.word_to_docs[k], words)
        res = reduce(set.intersection, word_to_docs)
        return list(res)

    def __eq__(self, other):
        return self.word_to_docs == other.word_to_docs

    @staticmethod
    def _set_default(obj):
        """set default"""
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    def dump(self, filepath, storage_policy=StoragePolicy):
        """Dump"""
        if storage_policy is None:
            with open(filepath, "w") as f:
                json.dump(self.word_to_docs, f, default=InvertedIndex._set_default)
        elif hasattr(storage_policy, "dump"):
            storage_policy.dump(filepath, self.word_to_docs)
        else:
            raise AttributeError("storage_policy has not dump method")

    def update(self, word_to_docs):
        """Update"""
        self.word_to_docs = word_to_docs
        self.number_of_words = len(word_to_docs.keys())

    @classmethod
    def load(cls, filepath, storage_policy=StoragePolicy):
        """Load"""
        inverted_index = InvertedIndex()
        if storage_policy is None:
            with open(filepath, "r") as f:
                word_to_docs = defaultdict(set, {k: set(v) for k, v in json.load(f).items()})
                inverted_index.update(word_to_docs)
        elif hasattr(storage_policy, "load"):
            word_to_docs = storage_policy.load(filepath)
            inverted_index.update(word_to_docs)
        else:
            raise AttributeError("storage_policy has not load method")
        return inverted_index


def callback_build(arguments):
    """Callback build"""
    documents = load_documents(arguments.dataset)
    inverted_index = build_inverted_index(documents)
    inverted_index.dump(arguments.output)


def callback_query(arguments):
    """Callback query"""
    inverted_index = InvertedIndex.load(arguments.index)
    if arguments.query:
        for q in arguments.query:
            res = inverted_index.query(q)
            print(",".join(res))
    else:
        for query in arguments.query_file:
            words = query.strip().split()
            res = inverted_index.query(words)
            print(",".join(res))


def setup_parser(parser):
    """Setup parser"""
    subparsers = parser.add_subparsers(
        help="choose command"
    )

    build_parser = subparsers.add_parser(
        "build",
        help="build inverted index and save in binary format into hard drive",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    build_parser.add_argument(
        "-d", "--dataset",
        default=DEFAULT_DATASET_PATH,
        help="path to dataset to load",
    )
    build_parser.add_argument(
        "-o", "--output",
        default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        help="path to store inverted index in a binary format",
    )
    build_parser.set_defaults(callback=callback_build)

    query_parser = subparsers.add_parser(
        "query",
        help="query inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    query_parser.add_argument(
        "-i", "--index", required=True,
        default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        help="path to read inverted index in a binary form",
    )
    query_parser.add_argument(
        "-q", "--query",
        nargs="+",
        action="append",
        help='query to run against inverted index',
    )
    query_file_group = query_parser.add_mutually_exclusive_group(required=False)
    query_file_group.add_argument(
        "--query-file-utf8", dest="query_file", type=EncodedFileType("r", encoding="utf8"),
        default=TextIOWrapper(sys.stdin.buffer, encoding="utf-8"),
        help="query file to get queries for inverted index",
    )
    query_file_group.add_argument(
        "--query-file-cp1251", dest="query_file", type=EncodedFileType("r", encoding="cp1251"),
        default=TextIOWrapper(sys.stdin.buffer, encoding="cp1251"),
        help="query file to get queries for inverted index",
    )
    query_parser.set_defaults(callback=callback_query)


def main() -> None:
    """Main"""
    parser = ArgumentParser(
        prog="inverted-index",
        description="tool to build, dump, load and query inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
