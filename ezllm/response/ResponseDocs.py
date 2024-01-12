from typing import Generic, List, TypeVar
from ezllm.Documents import Document


R = TypeVar('R', bound='ResponseDoc')

class ResponseDoc(Document):
    from ezllm.SubDoc import SearchSubDocs, SubDocs, SubDoc

    subdocs: SubDocs[SubDoc]
    SubDocsClass = SubDocs[SubDoc]
    def __init__(self, doc):
        super().__init__(
            data=doc
        )

    def __repr__(self, indent=28):
        ind = ' ' * indent

        return f"""\
{self.__class__.__name__}(
{ind}name={self.name}
{ind}SubDocs={len(self.subdocs)}
{" " * 24})"""

class SearchResponseDoc(ResponseDoc):
    from ezllm.SubDoc import SearchSubDocs, SubDocs
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
    
    def __repr__(self, indent=20):
        ind = ' ' * indent
        nested_repr = (' ' * (indent+4)) + ("\n" + ind).join([repr(obj) for obj in self.docs])

        return f"""\
{self.__class__.__name__}(
{ind}docs=[
{nested_repr}
{ind}]
{' ' * 16})"""
    
class SearchResponseDocs(ResponseDocs[SearchResponseDoc]):
    DocClass = SearchResponseDoc