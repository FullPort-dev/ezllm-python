import json
from typing import Generic, List, TypeVar, overload
import requests

from ezllm.Client import Client
from ezllm.Filter import Filter
from ezllm.methods import ExtractionMethod, QAMethod
from ezllm.methods.Base import MethodBase
from ezllm.response import ExtractionMethodResponse, QAMethodResponse, ResponseDoc
from ezllm.response.Base import ResponseBase
from ezllm.types import GroupTypes

T = TypeVar('T', bound=ResponseBase)

class RetrievalBase(Generic[T]):
    ResponseClass: T = ResponseBase
    def __init__(
        self,
        client: Client,
        filter,
        group: GroupTypes=GroupTypes,
    ):
        self.client = client or Client()
        self.filter = filter or Filter()
        self.group = group
        self.output: T = None
    
    @overload
    def run(self, method: QAMethod) -> QAMethodResponse:
        pass

    @overload
    def run(self, method:ExtractionMethod) -> ExtractionMethodResponse:
        pass

    def run(self, method: MethodBase):
        data = {
            **self.json(),
            **method.json(),
        }
        body = json.dumps(data, indent=4)
        res = requests.post(f'{self.client.workspace_run_url}/run', data=body, headers=self.client.headers)
        output = res.json()

        return method.format_response(output)
    
    def get(self) -> T:
        url = f"{self.client.workspace_run_url}/retrieve"
        body = json.dumps(
            self.json()
        )
        response = requests.post(url, data=body, headers=self.client.headers)
        if response.status_code == 200:
            data = response.json()
            self.data = data
            self.output = self.ResponseClass(data)
            return self.output
        else:
            print("Error: ", response.status_code)
        
        
    def json(self):
        raise NotImplementedError()
    

    def get_cache(self):
        if self.output:
            return self.output
        self.get()
        return self.output
    
    @property
    def docs(self) -> List[ResponseDoc]:
        self.get_cache()
        return self.output.docs
    

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)

        return f"""\
{self.__class__.__name__}(
{ind}output={self.output.__repr_nested__(indent+4) if self.output else None}
{ind}retrieval={self.json()}
{" " * (indent)})"""