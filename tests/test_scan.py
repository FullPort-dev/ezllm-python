from ezllm import Document
from tests.constants import TEST_DOC_ID


def test_scan_document():
    doc = Document(TEST_DOC_ID)
    output = doc.scan()
    data = output.get()
    docs = data.docs
    data.costs
    assert len(docs) == 1


def test_scan_filter_no_get():
    doc = Document(TEST_DOC_ID)
    output = doc.filter().scan()
    docs = output.docs
    output.output.costs

    assert len(docs) == 1