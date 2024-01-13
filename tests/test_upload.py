import time
import ezllm
from ezllm import Collection



def test_upload_path():
    doc = ezllm.upload(path='./tests/data/test_doc.md')
    assert doc.state == 'active'

def test_upload_file():
    file = open('./tests/data/test_doc.md', 'r')
    col = Collection(name="Default Collection")
    doc = col.upload(file)

    assert doc.name == 'test_doc.md'
    assert doc.state == 'active'

def test_upload_dont_await_processed():
    file = open('./tests/data/test_doc.md', 'r')
    col = Collection(name="Default Collection")
    doc = col.upload(file=file, await_processed=False)
    print("start doc state", doc.state)
    assert doc.state == 'unprocessed'
    time.sleep(2)
    state = doc.get_state()
    assert state == 'active'
    print("end doc state", doc.state)
    assert doc.state == 'active' # make sure that the objects reference has been updated

