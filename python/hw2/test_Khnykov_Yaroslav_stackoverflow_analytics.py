import pytest
from textwrap import dedent
from task_Khnykov_Yaroslav_stackoverflow_analytics import (
    StackoverflowAnalyzer, callback_analyze, NoStopWordsError
)

DATASET_TINY_STR = dedent("""\
    <row Id="4187367" PostTypeId="1" CreationDate="2019" Score="10" Title="Is SEO better done with repetition?" />	
    <row Id="4187368" PostTypeId="1" CreationDate="2019" Score="5" Title="What is SEO?" />	
    <row Id="4187369" PostTypeId="1" CreationDate="2020" Score="20" Title="Is Python better than Javascript?" />
""")
DATASET_BROKEN_STR = "Broken"
DATASET_NO_ATTR_STR = dedent("""\
    <row Id="4187367" Score="10" Title="Is SEO better done with repetition?" />	
    <row Id="4187368" PostTypeId="1" CreationDate="2019" Score="5" Title="What is SEO?" />	
    <row Id="4187369" PostTypeId="2" CreationDate="2020" Score="20" Title="Is Python better than Javascript?" />
""")
STOPWORDS_STR = dedent("""\
    a
    better
    c
""")
QUERIES_STR = dedent("""\
    2019,2019,2
    2019,2020,4
    2019,2020,100
""")


@pytest.fixture()
def dataset_tiny_fio(tmpdir):
    dataset_fio = tmpdir.join("tiny_dataset.txt")
    dataset_fio.write(DATASET_TINY_STR)
    return dataset_fio


@pytest.fixture()
def dataset_broken_fio(tmpdir):
    dataset_fio = tmpdir.join("broken_dataset.txt")
    dataset_fio.write(DATASET_BROKEN_STR)
    return dataset_fio


@pytest.fixture()
def dataset_no_attr_fio(tmpdir):
    dataset_fio = tmpdir.join("no_attr_dataset.txt")
    dataset_fio.write(DATASET_NO_ATTR_STR)
    return dataset_fio


@pytest.fixture()
def stopwords_fio(tmpdir):
    stpwrds_fio = tmpdir.join("stpwrds.txt")
    stpwrds_fio.write(STOPWORDS_STR)
    return stpwrds_fio


@pytest.fixture()
def queries_fio(tmpdir):
    qrs_fio = tmpdir.join("queries")
    qrs_fio.write(QUERIES_STR)
    return qrs_fio


def test_analyzer_can_initialize():
    StackoverflowAnalyzer()


def test_analyzer_can_read_from_file(dataset_tiny_fio):
    StackoverflowAnalyzer.read_xml(dataset_tiny_fio)


def test_analyzer_can_read_from_file_check_attr(dataset_tiny_fio):
    StackoverflowAnalyzer.read_xml(dataset_tiny_fio, check_attrib_values={"PostTypeId": "1"})


def test_analyzer_can_load_stopwords(stopwords_fio):
    azr = StackoverflowAnalyzer()
    azr.load_stopwords(stopwords_fio)


def test_analyzer_raises_when_no_stopwords(dataset_tiny_fio):
    azr = StackoverflowAnalyzer.read_xml(dataset_tiny_fio)
    with pytest.raises(NoStopWordsError):
        azr.analyze(5, year_from=2019, year_to=2020, check_stopwords=True)


def test_analyzer_can_handle_no_attr(dataset_no_attr_fio):
    StackoverflowAnalyzer.read_xml(dataset_no_attr_fio, check_attrib_values={"PostTypeId": "1"})


def test_analyzer_can_handle_broken_strings(dataset_broken_fio):
    StackoverflowAnalyzer.read_xml(dataset_broken_fio)


def test_analyzer_can_analyze_dataset(dataset_tiny_fio):
    azr = StackoverflowAnalyzer.read_xml(dataset_tiny_fio)
    azr.analyze(5, year_from=2019, year_to=2020)


def test_analyzer_can_analyze_broken_dataset(dataset_broken_fio):
    azr = StackoverflowAnalyzer.read_xml(dataset_broken_fio)
    azr.analyze(5, year_from=2019, year_to=2020)


def test_analyzer_filter_stopwords(dataset_tiny_fio, stopwords_fio):
    azr = StackoverflowAnalyzer.read_xml(dataset_tiny_fio)
    azr.load_stopwords(stopwords_fio)
    azr.analyze(5, year_from=2019, year_to=2020, check_stopwords=True)


def test_analyzer_can_handle_big_topn(dataset_tiny_fio, stopwords_fio):
    azr = StackoverflowAnalyzer.read_xml(dataset_tiny_fio)
    azr.analyze(100, year_from=2019, year_to=2020)


@pytest.fixture()
def arguments(dataset_tiny_fio, stopwords_fio, queries_fio):
    class Arguments:
        def __init__(self):
            self.questions = dataset_tiny_fio
            self.stop_words = stopwords_fio
            self.queries = queries_fio
    return Arguments()


def test_callback_analyze(arguments):
    callback_analyze(arguments)
