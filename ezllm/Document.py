import time
from typing import TYPE_CHECKING, Dict, Generic, TypeVar, overload
from ezllm.Entity import Entity

from ezllm.SubDoc import SubDocs
from ezllm.constants import UPLOAD_TIMEOUT

if TYPE_CHECKING:
    from ezllm.methods.Base import MethodBase
    from ezllm.methods import ExtractionMethod, QAMethod
    from ezllm.response import ExtractionMethodResponse, QAMethodResponse

import requests
from ezllm.types import DocumentStateTypes, GroupTypes, MetadataFilterType

from ezllm.errors import FileProcessingError, NotFound
from .Client import Client

S = TypeVar('S', bound=SubDocs)

class Document(Generic[S], Entity):
    subdocs: S
    SubDocsClass: S = SubDocs
    def __init__(
            self,
            id = None,
            client:Client = None,
            data: Dict = None,
        ):
        super().__init__(id=id, data=data, client=client)
        self.subdocs = self.SubDocsClass(self, self._data.get('subdocs', []))
        
        
    def get_state(self) -> DocumentStateTypes:
        res = requests.get(
            f'{self.url}/state',
            headers=self.client.headers,
        )
        state = res.json()
        self._data['state'] = state
        return state

    @property
    def url(self):
        return f'{self.client.workspace_api_url}/d/{self._id}'
    
    def filter(self,
            metadata: 'MetadataFilterType' = {}
        ):

        from .Filter import Filter
        return Filter(documents=[self], metadata=metadata)

    def search(
            self,
            query,
            group: GroupTypes = 'all',
            n_docs = 10
        ):
        from .Search import SearchRetrieval
        return SearchRetrieval(
            client=self.client,
            query=query,
            n_docs=n_docs,
            filter=self.filter(),
            group=group
        )

    def scan(
            self,
            group: GroupTypes = 'all',
        ):
        from .Scan import ScanRetrieval
        return ScanRetrieval(
            client=self.client,
            group=group,
            filter=self.filter()
        )
    
    @overload
    def run(
            self,
            method: 'ExtractionMethod' = None,
            group: GroupTypes = 'all',
            include_docs: bool = False,
        ) -> 'ExtractionMethodResponse': ...

    @overload
    def run(
            self,
            method: 'QAMethod' = None,
            group: GroupTypes = 'all',
            include_docs: bool = False,
        ) -> 'QAMethodResponse': ...
        
    def run(
            self,
            method: 'MethodBase' = None,
            group: GroupTypes = 'all',
            include_docs: bool = False,
        ):
        return self.scan(group).run(method, include_docs=include_docs)

    def delete(self):
        headers = {
            "Content-Type": "application/json",
            **self.client.headers  
        }
        res = requests.delete(
            self.url,
            headers=headers,
        )
        self._data = res.json()
        return self

    def await_processed(self):
        MAX_POLLING_INTERVAL = 10
        interval = 1
        start = time.time()
        while True:
            if time.time() - start > UPLOAD_TIMEOUT:
                raise TimeoutError("Polling timed out")
            time.sleep(interval)
            state = self.get_state()
            interval = min(interval*2, MAX_POLLING_INTERVAL)

            if state == 'active':
                break
            if state == 'error':
                raise FileProcessingError()

    @property
    def name(self) -> str:
        return self.data['name']
    
    @property
    def state(self) -> str:
        return self.data['state']

    def __repr__(self):
        return self.__repr_nested__(indent=0)    

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)
        nested_ind = ' ' * (indent+8)
        
        if indent < 8:
            subdocs_repr = f"[\n{nested_ind}{self.subdocs.__repr_nested__(indent+4)}\n{nested_ind}]"
        else:
            subdocs_repr = 'SubDocs(...)'
        return f"""\
{self.__class__.__name__}(
{ind}id={self.id}
{ind}name={self.name}
{ind}state={self.state}
{ind}subdocs={subdocs_repr}
{" " * (indent)})"""