from dataclasses import dataclass
from typing import Generic, List, TypeVar
from ezllm.response.Costs import ResponseCosts
from ezllm.response.ResponseDocs import ResponseDocs
from ezllm.response.DocOutputGroup import DocOutputGroups
from ezllm.response.OutputGroup import OutputData, OutputGroups

O = TypeVar('O', bound=OutputGroups)
DT = TypeVar('DT', bound=OutputData)


class ResponseBase(Generic[O]):
    DocGroupClass = DocOutputGroups
    def __init__(self, data):
        self.costs = ResponseCosts(data['costs'], data['total_cost'])
        self.duration = data['duration']
        self.doc_groups: O = self.DocGroupClass(data['doc_groups'])

    @property
    def docs(self):
        return ResponseDocs(docs=self.doc_groups.data)

    def __repr__(self, indent=4) -> str:
        ind = " " * indent
        return f"""\
{self.__class__.__name__}(
{ind}costs={self.costs}
{ind}doc_groups={self.doc_groups}
)"""


class MethodResponse(ResponseBase[DocOutputGroups], Generic[O, DT]):
    OutputGroupsClass: O = OutputGroups
    def __init__(self, data):
        super().__init__(data)
        self.output: O = self.OutputGroupsClass(data['output_groups'])
    
    @property
    def data(self) -> List[DT]:
        return self.output.data
    
    def __repr__(self, indent=4) -> str:
        ind = " " * indent
        return f"""\
{self.__class__.__name__}(
{ind}costs={self.costs}
{f"{ind}# add the include_docs=True argument to return docs" if len(self.doc_groups) == 0 else ""}
{ind}doc_groups={self.doc_groups}
{ind}output_groups={self.output}
)"""