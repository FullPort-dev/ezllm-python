from dataclasses import dataclass
from typing import Dict, Generic, List, TypeVar
from ezllm.response.Costs import ResponseCosts
from ezllm.response.ResponseDocs import ResponseDocs
from ezllm.response.DocOutputGroup import DocOutputGroups
from ezllm.response.OutputGroup import OutputData, OutputGroups

O = TypeVar('O', bound=DocOutputGroups)
DT = TypeVar('DT', bound=OutputData)


class ResponseBase(Generic[O]):
    doc_groups: DocOutputGroups
    DocGroupClass = DocOutputGroups
    def __init__(self, data: Dict):
        self.costs = ResponseCosts(data['costs'], data['total_cost'])
        self.duration = data['duration']
        self.doc_groups: O = self.DocGroupClass(data.get('doc_groups', []))

    @property
    def docs(self):
        return self.doc_groups.docs

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0) -> str:
        ind = " " * (indent+4)
        return f"""\
{self.__class__.__name__}(
{ind}costs={self.costs.__repr_nested__(indent+4)}
{ind}doc_groups={self.doc_groups.__repr_nested__(indent+4)}
{' ' * indent})"""


class MethodResponse(ResponseBase[DocOutputGroups], Generic[O, DT]):
    OutputGroupsClass: O = OutputGroups
    def __init__(self, data):
        super().__init__(data)
        self.output: O = self.OutputGroupsClass(data.get('output_groups', []))
    
    @property
    def data(self) -> List[DT]:
        return self.output.data

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0) -> str:
        ind = " " * (indent+4)
        return f"""\
{self.__class__.__name__}(
{ind}costs={self.costs.__repr_nested__(indent+4)}
{f"{ind}# add the include_docs=True argument to return docs" if len(self.doc_groups) == 0 else ""}
{ind}doc_groups={self.doc_groups.__repr_nested__(indent+4)}
{ind}output_groups={self.output.__repr_nested__(indent+4)}
)"""