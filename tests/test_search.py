from ezllm import Collection
from ezllm.Document import Document
from tests.constants import TEST_COL_ID, TEST_DOC_ID


def test_search_document():
    doc = Document(TEST_DOC_ID)
    search_retrieval = doc.search("Hiking and dogs", n_docs=3)
    output = search_retrieval.get()
    # output is SearchResponse because of the .get()
    docs = output.docs
    print(search_retrieval)
    assert len(docs) == 1


def test_search_document_no_get():
    """
    in this case we're testing that we can load the data from the .docs property
    without having to call the .get()
    """
    doc = Document(TEST_DOC_ID)
    search_retrieval = doc.search("Hiking and dogs", n_docs=3)
    # output is SearchRetrieval because of the lack of .get()
    # this means that you won't have access to .costs until you do .get()
    docs = search_retrieval.docs
    doc = docs[0]
    for subdoc in doc.subdocs:
        print("iterating through subdocs", subdoc)
        assert subdoc.index == 0
    tmp = doc.subdocs[0]

    assert tmp.index == 0
    assert type(tmp.content) == str
    assert doc.name == 'Reddit Test File'
    assert len(docs) == 1


def test_search_filter():
    doc = Document(TEST_DOC_ID)
    output = doc.filter({'index':0}).search("Hiking and dogs", n_docs=3)
    docs = output.docs
    doc = docs[0]
    assert doc.name == 'Reddit Test File'
    assert len(docs) == 1


def test_collection_search():
    col = Collection(TEST_COL_ID)
    retrieval = col.search('Hello World')
    assert retrieval._output == None
    retrieval.get()
    assert retrieval.output is not None
    docs = retrieval.get()
    print(retrieval)
    print(docs)