from typing import Generic, List, TypeVar
from ezllm.Documents import Document
from ezllm.SubDoc import SearchSubDocs, SubDocs, SubDoc


R = TypeVar('R', bound='ResponseDoc')

class ResponseDoc(Document):

    subdocs: SubDocs[SubDoc]
    SubDocsClass = SubDocs[SubDoc]
    def __init__(self, doc):
        super().__init__(
            data=doc
        )

    def __repr__(self):
        return self.__repr_nested__(indent=0)

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent + 4)

        return f"""\
{self.__class__.__name__}(
{ind}name={self.name}
{ind}SubDocs={len(self.subdocs)}
{" " * indent})"""

class SearchResponseDoc(ResponseDoc):
    subdocs: SearchSubDocs
    SubDocsClass = SearchSubDocs


class ResponseDocs(Generic[R]):
    DocClass: R = ResponseDoc
    def __init__(self, data=[], docs: List[R]=None):
        self.docs: List[R] = []
        if docs is not None:
            self.docs = docs
        else:
            for d in data:
                self.docs.append(self.DocClass(d))
        
    def by_id(self, id: str):
        for doc in self.docs:
            if doc.id == id:
                return doc
            
        return None
    
    @property
    def data(self):
        return self.docs

    def __len__(self):
        return len(self.docs)

    def __getitem__(self, index) -> R:
        return self.docs[index]
    
    def __reversed__(self) -> List[R]:
        return reversed(self.docs)
    
    def __iter__(self):
        return iter(self.docs)

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)
        nested_repr = (' ' * (indent+8)) + ("\n" + (' ' *(indent+8))).join([obj.__repr_nested__(indent+8) for obj in self.docs])

        return f"""\
{self.__class__.__name__}(
{ind}docs=[
{nested_repr}
{ind}]
{' ' * indent})"""
    
class SearchResponseDocs(ResponseDocs[SearchResponseDoc]):
    DocClass = SearchResponseDoc