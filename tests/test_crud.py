import pytest
import ezllm
from ezllm.Collection import Collection
from ezllm.Collection import Document



def test_create_collection():
    Collection.create("Amogus1")
    
# def test_remove_collection():
    # Collection
    
def test_update_collection():
    col = Collection(name="Amogus2")
    col.update("Amogus3")

def test_delete_collection():
    # insure it doesn't exist at the start
    with pytest.raises(Exception):
        col = Collection(name="Delete Me!")
        col.get()

    # create then immediately delete
    Collection.create(name="Delete Me!").delete()

    # insure it doesn't exist at the end
    with pytest.raises(Exception):
        col = Collection(name="Delete Me!")
        col.get()


def test_delete_doc():
    file = open('./tests/data/test_doc.md', 'r')
    col = Collection(name="Default Collection")
    doc = col.upload(file=file, await_processed=False)
    doc = Document(id=doc.id)
    assert doc.state == 'unprocessed'

    doc.await_processed()
    assert doc.state == 'active'
    doc.delete()
    assert doc.state == 'deleted'

    print(doc.state)