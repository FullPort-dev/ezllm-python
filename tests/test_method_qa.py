from ezllm.Documents import Document
from ezllm.methods import QAMethod
from tests.constants import TEST_DOC_ID

def test_qa():
    doc = Document(TEST_DOC_ID)
    method = QAMethod(questions=["What is this data?", "What is the top post?"])
    response = doc.scan().run(method)



    
    print(response)
    print(response.output)

"""
No need to test doc.run() as it's just a wrapper around this
+ this operation isn't free
"""