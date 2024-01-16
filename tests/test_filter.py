import ezllm
from ezllm.Document import Document
from tests.constants import TEST_COL_ID, TEST_DOC_ID

"""
TODO
- collections
- test meta data
- different file types
"""


def test_filter_document():
    doc = Document(TEST_DOC_ID)
    output = doc.filter()
    print("OUTPUT", output)
    filter_data = output.get()
    docs = filter_data.docs
    print("OUTPUT", output)

    g = filter_data.doc_groups.groups[0]
    g # OutputGroup
    g.data
    assert len(docs) == 1


def test_filter_document_no_get():
    """
    in this case we're testing that we can load the data from the .docs property
    without having to call the .get()
    """
    doc = Document(TEST_DOC_ID)
    output = doc.filter()
    docs = output.docs
    doc = docs[0]
    assert doc.name == 'Reddit Test File'
    assert len(docs) == 1


def test_filter_document_id():
    output = ezllm.filter(documents=[TEST_DOC_ID])
    docs = output.docs
    doc = docs[0]
    assert doc.name == 'Reddit Test File'
    assert len(docs) == 1


def test_filter_document_id():
    output = ezllm.filter(documents=[TEST_DOC_ID])
    docs = output.docs
    doc = docs[0]
    assert doc.name == 'Reddit Test File'
    assert len(docs) == 1

def test_filter_collection_id():
    output = ezllm.filter(collections=[TEST_COL_ID])
    docs = output.docs
    doc = docs[0]
    assert doc.name == 'Reddit Test File'
    assert len(docs) == 1