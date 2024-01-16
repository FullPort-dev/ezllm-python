from ezllm import Collection, Document
from ezllm.Collections import Collections
from tests.constants import TEST_COL_ID, TEST_DOC_ID


def test_repr_subdocs_hidden():
    cols = Collections()
    col = Collection(TEST_COL_ID)
    doc = Document(TEST_DOC_ID)
    cols_repr = str(cols)
    col_repr = str(col)
    doc_repr = str(doc)
    print(cols_repr)
    print(col_repr)
    print(doc_repr)
    assert 'subdocs=[' in doc_repr
    assert 'SubDocs(...)' in col_repr
    # c = Collections()
    # _repr = str(c)
    # print(_repr)