import os
from ezllm import Client, Collection, Document
from .constants import TEST_COL_ID, TEST_DOC_ID

def test_init_client():
    c = Client()
    print(c)
    assert c != None


def test_init_collection():
    collection = Collection(id=TEST_COL_ID)
    data = collection.get()
    assert 'test' == data['name']
    assert TEST_COL_ID == data['_id']

def test_init_collection_by_name():
    collection = Collection(name="test")
    data = collection.get()
    assert collection._name == data['name']


def test_init_document():
    document = Document(id=TEST_DOC_ID)
    document.get()
    assert 'Reddit Test File' == document.name
    assert 'active' == document.state
    assert TEST_DOC_ID == document.id