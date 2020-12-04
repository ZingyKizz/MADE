from textwrap import dedent
import pytest
from task_Khnykov_Yaroslav_inverted_index import (
    EncodedFileType, StoragePolicy, InvertedIndex, build_inverted_index, load_documents, main, callback_query,
    callback_build
)

DATASET_BIG_FILEPATH = "wikipedia_sample.txt"
DATASET_SMALL_FILEPATH = "small_wikipedia_sample.txt"
DATASET_TINY_FILEPATH = "tiny_wikipedia_sample.txt"
DATASET_TINY_STR = dedent("""\
    123 some words A_word and nothing
    2   some word B_word in this dataset
    5   famous_phrases to be or not to be
    37  all words such as A_word and B_word are here
""")


@pytest.fixture()
def dataset_tiny_expected_documents():
    return {
        "123": "some words A_word and nothing",
        "2": "some word B_word in this dataset",
        "5": "famous_phrases to be or not to be",
        "37": "all words such as A_word and B_word are here"
    }


def test_can_load_documents_from_dataset_tiny(dataset_tiny_expected_documents):
    documents = load_documents(DATASET_TINY_FILEPATH)
    assert documents == dataset_tiny_expected_documents, (
        "load_documents incorrectly loaded dataset"
    )


@pytest.fixture()
def dataset_tiny_fio(tmpdir):
    dataset_fio = tmpdir.join("tiny_dataset.txt")
    dataset_fio.write(DATASET_TINY_STR)
    return dataset_fio


def test_can_load_documents(dataset_tiny_fio, dataset_tiny_expected_documents):
    documents = load_documents(dataset_tiny_fio)
    assert documents == dataset_tiny_expected_documents, (
        "load_documents incorrectly loaded dataset"
    )


@pytest.mark.parametrize(
    "query, expected_res",
    [
        pytest.param(["A_word"], ["123", "37"], id="A_word"),
        pytest.param(["B_word"], ["2", "37"], id="B_word"),
        pytest.param(["A_word", "B_word"], ["37"], id="both words"),
        pytest.param(["this_word_doesnt_exists"], [], id="this word doesnt exists")
    ]
)
def test_query_inverted_index_intersect_results(dataset_tiny_fio, query, expected_res):
    documents = load_documents(dataset_tiny_fio)
    tiny_inverted_index = build_inverted_index(documents)
    res = tiny_inverted_index.query(query)
    assert sorted(res) == sorted(expected_res)


def test_can_load_big_dataset():
    documents = load_documents(DATASET_BIG_FILEPATH)
    assert len(documents) == 4100, (
        "incorrectly loaded Wikipedia sample"
    )


@pytest.fixture()
def wikipedia_documents():
    documents = load_documents(DATASET_BIG_FILEPATH)
    return documents


@pytest.fixture()
def small_sample_wikipedia_documents():
    documents = load_documents(DATASET_SMALL_FILEPATH)
    return documents


def test_can_build_and_query_inverted_index(wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(wikipedia_documents)
    doc_ids = wikipedia_inverted_index.query(["wikipedia"])
    assert isinstance(doc_ids, list), (
        "inverted index query should return list"
    )


@pytest.fixture()
def wikipedia_inverted_index(wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(wikipedia_documents)
    return wikipedia_inverted_index


@pytest.fixture()
def small_wikipedia_inverted_index(small_sample_wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(small_sample_wikipedia_documents)
    return wikipedia_inverted_index


@pytest.mark.parametrize(
    "storage_policy",
    [
        pytest.param(None, id="dump without storage policy"),
        pytest.param(StoragePolicy, id="dump with storage policy")
    ]
)
def test_can_dump_inverted_index(storage_policy, tmpdir, wikipedia_inverted_index):
    index_fio = tmpdir.join("index_dump.txt")
    wikipedia_inverted_index.dump(index_fio, storage_policy)


def test_can_dump_and_load_inverted_index(tmpdir, wikipedia_inverted_index):
    index_fio = tmpdir.join("index_dump.txt")
    wikipedia_inverted_index.dump(index_fio)
    loaded_inverted_index = InvertedIndex.load(index_fio)
    assert wikipedia_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


@pytest.mark.parametrize(
    "filepath",
    [
        pytest.param(DATASET_SMALL_FILEPATH, id="small dataset"),
        pytest.param(DATASET_BIG_FILEPATH, id="big dataset")
    ]
)
def test_can_dump_and_load_inverted_index_with_array_policy_parametrized(filepath, tmpdir):
    index_fio = tmpdir.join("index.dump")
    documents = load_documents(filepath)
    expected_inverted_index = build_inverted_index(documents)
    expected_inverted_index.dump(index_fio, storage_policy=StoragePolicy)
    loaded_inverted_index = InvertedIndex.load(index_fio, storage_policy=StoragePolicy)
    assert expected_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


def test_raise_set_default_with_incorrect_type(small_wikipedia_inverted_index):
    with pytest.raises(TypeError):
        small_wikipedia_inverted_index._set_default(1)


def test_raise_dump(tmpdir, small_wikipedia_inverted_index):
    with pytest.raises(AttributeError):
        small_wikipedia_inverted_index.dump(tmpdir, 3)


def test_can_repr(small_wikipedia_inverted_index):
    assert isinstance(repr(small_wikipedia_inverted_index), str)


def test_can_load_without_storage_policy(tmpdir, filepath=DATASET_SMALL_FILEPATH):
    index_fio = tmpdir.join("index.dump")
    documents = load_documents(filepath)
    expected_inverted_index = build_inverted_index(documents)
    expected_inverted_index.dump(index_fio, storage_policy=None)
    InvertedIndex.load(index_fio, storage_policy=None)


def test_can_load_without_storage_policy(tmpdir, filepath=DATASET_SMALL_FILEPATH):
    index_fio = tmpdir.join("index.dump")
    documents = load_documents(filepath)
    expected_inverted_index = build_inverted_index(documents)
    expected_inverted_index.dump(index_fio, storage_policy=None)
    InvertedIndex.load(index_fio, storage_policy=None)


def test_can_raise_without_storage_policy(tmpdir, filepath=DATASET_SMALL_FILEPATH):
    index_fio = tmpdir.join("index.dump")
    documents = load_documents(filepath)
    expected_inverted_index = build_inverted_index(documents)
    expected_inverted_index.dump(index_fio, storage_policy=None)
    with pytest.raises(AttributeError):
        InvertedIndex.load(index_fio, storage_policy=3)


@pytest.fixture()
def arguments(small_wikipedia_inverted_index, tmpdir, filepath=DATASET_SMALL_FILEPATH):
    index_fio = tmpdir.join("index.dump")
    documents = load_documents(filepath)
    expected_inverted_index = build_inverted_index(documents)
    expected_inverted_index.dump(index_fio, storage_policy=StoragePolicy)

    class Arguments:
        def __init__(self):
            self.dataset = DATASET_SMALL_FILEPATH
            self.index = index_fio
            self.output = index_fio
            self.query = [["a", "b"]]

    return Arguments()


def test_callback_query(arguments):
    callback_query(arguments)


def test_callback_build(arguments):
    callback_build(arguments)


def test_main():
    with pytest.raises(AttributeError):
        main()


def test_encoded():
    EncodedFileType("-")
