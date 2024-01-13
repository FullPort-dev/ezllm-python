from typing import TYPE_CHECKING, Any, Generic, List, TypeVar

import requests

from ezllm.errors import NotFound
if TYPE_CHECKING:
    from ezllm.Documents import Document

S = TypeVar('S', bound='SubDoc')

class SubDoc:
    def __init__(self, data):
        self._data = data
        self.content = data.get('page_content')
        self.metadata = data.get('metadata')
        _metadata = data.get('metadata', {})
        self.index = _metadata.get('index')
        self.page = _metadata.get('page')

        # TODO how to access .page (PDF specific metadata)
        # I'm just going to export all of them
        # it would be impossible (without generics) to 
        # determine the doc type

    def __repr__(self):
        return self.__repr_nested__(indent=0)

    def __repr_nested__(self, indent=0):
        ind = ' ' * indent
        return f"""\
{self.__class__.__name__}(
{ind}content=\"\"\"
{self.content[0:500]}

{"(MORE CONTENT ...)" if len(self.content) > 500 else ""}
\"\"\"
{ind}metadata={self.metadata}
{ind}]
{" " * (indent-4)})"""

class SearchSubDoc(SubDoc):
    def __init__(self, data):
        super().__init__(data)
        self.score = self._data["score"]

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * indent
        return f"""\
{self.__class__.__name__}(
score={self.score}
{ind}content=\"\"\"
{self.content[0:500]}

{"(MORE CONTENT ...)" if len(self.content) > 500 else ""}
\"\"\"
{ind}metadata={self.metadata}
{ind}]
{" " * (indent-4)})"""

class SubDocs(Generic[S]):
    SubDocClass: S = SubDoc
    doc: 'Document'
    def __init__(
            self,
            doc,
            subdocs: List[Any]
        ) -> None:
        self.doc = doc
        self._subdocs: List[S] = [self.SubDocClass(x) for x in subdocs]
    
    @property
    def url(self):
        return f'{self.doc.url}/subdocs'
    
    def get(self):
        print(self.url)
        response = requests.get(
            self.url,
            headers=self.doc.client.headers,
        )
        if response.status_code == 200:
            # TODO format this into a Document
            data = response.json()
            self._subdocs = data

            return self
        else:
            print("ERROR FETCHING DOCUMENT", response.status_code)
            raise NotFound("Document")

    def get_cache(self):
        # TODO : basing load state off of data len is only temporary
        if len(self._subdocs) == 0:
            self.get()
        
        return self._subdocs
    
    @property
    def subdocs(self):
        return self.get_cache()

    def __len__(self):
        return len(self.subdocs)

    def __iter__(self):
        return iter(self.subdocs)
    
    def __getitem__(self, index: int) -> S:
        return self.subdocs[index]
    
    def __repr__(self):
        return self.__repr_nested__(indent=0)    

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)
        nested_repr = (' ' * (indent + 8)) + ("\n" + (' ' * (indent+8))).join([repr(obj) for obj in self.subdocs])

        return f"""\
{self.__class__.__name__}(
{ind}subdocs=[
{nested_repr}
{ind}]
{" " * (indent)})"""

    
class SearchSubDocs(SubDocs[SearchSubDoc]):
    subdocs: List[SearchSubDoc]
    SubDocClass = SearchSubDoc
