from typing import Generic, List, Optional, TypeVar

from ezllm.response.ResponseDocs import ResponseDocs, ResponseDoc, SearchResponseDoc, SearchResponseDocs
from ezllm.response.OutputGroup import OutputData, OutputGroups

D = TypeVar('D', bound='OutputData')

class DocOutputGroup(Generic[D]):
    OutputDataClass: D = ResponseDocs[ResponseDoc]

    def __init__(self, group):
        self._data: D = self.OutputDataClass(group['docs'])
        self.type = group['type']
        self.id: Optional[str] = group['id']

    @property
    def data(self) -> List[ResponseDoc]:
        return self._data.data

    def __repr__(self):
        return self.__repr_nested__(indent=0)

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)

        return f"""\
{self.__class__.__name__}(
{ind}id={self.id or 'None'}
{ind}type={self.type}
{ind}data={self._data.__repr_nested__(indent+4)}
{" " * indent})"""
    
    
class SearchDocOutputGroup(DocOutputGroup[SearchResponseDoc]):
    OutputDataClass: D = SearchResponseDocs


class DocOutputGroups(OutputGroups[DocOutputGroup[ResponseDocs[ResponseDoc]]]):
    OutputGroupClass = DocOutputGroup[ResponseDocs[ResponseDoc]]
            
class SearchDocOutputGroups(OutputGroups[SearchDocOutputGroup]):
    OutputGroupClass = SearchDocOutputGroup
    