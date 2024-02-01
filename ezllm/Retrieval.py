import json
from typing import Generic, List, TypeVar, overload
import requests

from ezllm.Client import Client
from ezllm.Filter import Filter
from ezllm.errors import handle_request_errors
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
        self._output: T = None
    
    @overload
    def run(
            self,
            method: QAMethod,
            include_docs: bool = False
        ) -> QAMethodResponse: ...

    @overload
    def run(
            self,
            method: ExtractionMethod,
            include_docs: bool = False
        ) -> ExtractionMethodResponse: ... 

    def run(
            self,
            method: MethodBase,
            include_docs: bool = False
        ):
        data = {
            'include_docs': include_docs,
            **self.json(),
            **method.json(),
        }
        body = json.dumps(data, indent=4)
        # print(body)
        res = requests.post(f'{self.client.workspace_run_url}/run', data=body, headers=self.client.headers)
        handle_request_errors(res)

        output = res.json()

        return method.format_response(output)
    
    def get(self) -> T:
        url = f"{self.client.workspace_run_url}/retrieve"
        body = json.dumps(
            self.json()
        )
        res = requests.post(url, data=body, headers=self.client.headers)
        handle_request_errors(res)

        if res.status_code == 200:
            data = res.json()
            self.data = data
            self._output = self.ResponseClass(data)
            return self._output
        else:
            print("Error: ", res.status_code)
        
        
    def json(self):
        raise NotImplementedError()
    

    def get_cache(self):
        if self._output:
            return self._output
        self.get()
        return self._output
    
    @property
    def docs(self) -> List[ResponseDoc]:
        return self.output.docs
    
    @property
    def output(self):
        self.get_cache()
        return self._output

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)

        return f"""\
{self.__class__.__name__}(
{ind}output={self._output.__repr_nested__(indent+4) if self.output else None}
{ind}retrieval={self.json()}
{" " * (indent)})"""