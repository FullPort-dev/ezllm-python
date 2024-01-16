import os
from ezllm import Client, Collection, Document
from .constants import TEST_COL_ID, TEST_DOC_ID

def test_init_client():
    c = Client()
    print(c)
    assert c != None

    print(c.collections)


def test_init_collection():
    collection = Collection(id=TEST_COL_ID)
    data = collection.get()
    assert 'test' == data.name
    assert TEST_COL_ID == data.id

    assert collection.docs.load_state == 'unloaded'
    
    for doc in collection.docs:
        print(doc)
        assert isinstance(doc, Document)
    
    assert collection.docs.load_state == 'loaded'

def test_init_collection_no_kwarg():
    collection = Collection(TEST_COL_ID)
    data = collection.get()
    assert 'test' == data.name
    assert TEST_COL_ID == data.id

    assert collection.docs.state == 'unloaded'
    
    for doc in collection.docs:
        print(doc)
        assert isinstance(doc, Document)
    
    assert collection.docs.state == 'loaded'


def test_init_collection_by_name():
    collection = Collection(name="test")
    data = collection.get()
    assert collection._name == data.name


def test_init_document():
    document = Document(id=TEST_DOC_ID)
    document.get()
    print(document)
    assert 'Reddit Test File' == document.name
    assert 'active' == document.state
    assert TEST_DOC_ID == document.id
    # print(document.subdocs)
    assert len(document.subdocs) == 1