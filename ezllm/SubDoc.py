from typing import Generic, List, TypeVar

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

    def __repr__(self, indent=4):
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

    def __repr__(self, indent=4):
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
    def __init__(self, subdocs) -> None:
        self.subdocs: List[S] = [self.SubDocClass(x) for x in subdocs]

    def __len__(self):
        return len(self.subdocs)

    def __iter__(self):
        return iter(self.subdocs)
    
    def __getitem__(self, index: int) -> S:
        return self.subdocs[index]
    
    def __repr__(self, indent=0):
        ind = ' ' * indent
        nested_repr = (' ' * (indent + 4)) + ("\n" + (' ' * (indent+4))).join([repr(obj) for obj in self.subdocs])

        return f"""\
{self.__class__.__name__}(
{ind}subdocs=[
{nested_repr}
{ind}]
{" " * (indent-4)})"""
    
class SearchSubDocs(SubDocs[SearchSubDoc]):
    subdocs: List[SearchSubDoc]
    SubDocClass = SearchSubDoc
