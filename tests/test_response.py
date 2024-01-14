from ezllm.response import ExtractionMethodResponse
from ezllm.response.methods.ExtractionResponse import ExtractionOutputGroup
from ezllm.response import SearchResponse, ScanResponse, FilterResponse, QAMethodResponse, ResponseDoc
from tests.data.response import EXTRACTION_RESPONSE_DATA, FILTER_RESPONSE_DATA, QA_INCLUDE_DOCS_RESPONSE_DATA, QA_RESPONSE_DATA, SCAN_RESPONSE_DATA, SEARCH_RESPONSE_DATA
import pandas as pd

def test_extraction_response():
    response = ExtractionMethodResponse(EXTRACTION_RESPONSE_DATA)
    # print("OUTPUT", response.output_groups.groups[0].data)
    # print("OUTPUT", response.output[0])

    df = response.df
    dfs = response.dfs


    response.data
    response.output
    o = response.output[0]
    o2 = response.output.by_id('test_id')
    assert o2.id == 'test_id'
    
    g = response.output.groups[0]
    g.data
    print(response)

    assert type(g) == ExtractionOutputGroup
    assert 'posts' in dfs.keys()
    assert type(df) == pd.DataFrame
    assert dfs['posts']['upvotes'][2] == 2937


def test_qa_response():
    response = QAMethodResponse(QA_RESPONSE_DATA)
    print(response)
    doc = response.data[0]
    o = response.output.by_id("658b4e441f41ead7592562de")

    for question in response.data:
        assert type(question.question) == str
        assert type(question.answer) == str
        assert type(question.relevant) == int

    for group in response.output:
        d = group.data
        assert type(group.id) == str
        assert type(group.type) == str
        for question in group.questions:
            assert type(question.question) == str
            assert type(question.answer) == str
            assert type(question.relevant) == int

        for question in group.data:
            assert type(question['question']) == str
            assert type(question['answer']) == str
            assert type(question['relevant']) == int

    assert o.id == '658b4e441f41ead7592562de'
    assert response.data[0]['question'] == 'Who are the authors?'

def test_qa_include_docs_response():
    response = QAMethodResponse(QA_INCLUDE_DOCS_RESPONSE_DATA)
    print(response)
    question_data = response.data[0]
    print()
    o = response.output.by_id("658b4e441f41ead7592562de")


    for group in response.output:
        d = group.data
        assert type(group.id) == str
        assert type(group.type) == str
        for question in group.questions:
            assert type(question.question) == str
            assert type(question.answer) == str
            assert type(question.relevant) == int

        for question in group.data:
            assert type(question['question']) == str
            assert type(question['answer']) == str
            assert type(question['relevant']) == int

    assert o.id == '658b4e441f41ead7592562de'
    assert response.data[0]['question'] == 'Who are the authors?'



def test_filter_response():
    response = FilterResponse(FILTER_RESPONSE_DATA)
    print(response)

    docs = response.docs
    doc = docs[0]

    # there technically isn't such a thing as grouped output for filter
    for group in response.doc_groups:
        group

        
    assert doc.name == 'Reddit Test File'
    assert len(docs) == 1


def test_scan_response():
    response = ScanResponse(SCAN_RESPONSE_DATA)
    print(response)
    response.docs
    for doc in response.docs:
        assert type(doc) == ResponseDoc

    doc = response.docs.by_id("659a54a5d9569e7b627dea93")
    assert doc.id == '659a54a5d9569e7b627dea93'


def test_search_response():
    response = SearchResponse(SEARCH_RESPONSE_DATA)
    print(response)
    print(response.docs)
    doc = response.docs[0]
    subdoc = doc.subdocs[0]

    assert type(subdoc.score) == float
    



# def test_search_response():
#     pass