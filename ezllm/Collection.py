from enum import Enum
from io import BufferedReader
from typing import TYPE_CHECKING, Any, List, Optional, overload
from ezllm.Documents import Documents
from ezllm.Document import Document
from ezllm.Entity import Entity
from ezllm.errors import NotFound
from ezllm.types import GroupTypes
from .Client import Client
import mimetypes
import json
import requests

if TYPE_CHECKING:
    from ezllm.methods.Base import MethodBase
    from ezllm.methods import ExtractionMethod, QAMethod
    from ezllm.response import ExtractionMethodResponse, QAMethodResponse

class FileTypes(Enum):
    pdf='pdf'
    csv='csv'
    txt='txt'

class Collection(Entity):
    def __init__(
            self,
            id=None,
            client:Client=None,
            data = None,
            name=None,
        ):
        super().__init__(id=id, data=data, client=client)
        self._name = name
        self.docs = Documents(self, client=self.client)
        
    
    
    @classmethod
    def create(cls, name, client: Client = None):
        client = client or Client()
        url = f'{client.workspace_api_url}/c'
        data = {
                # "id": "string",
                "name": name,
                # "groups": [],
                # "visibility": "private"
        }
        headers = {
            "Content-Type": "application/json",
            **client.headers  
        }
        res = requests.post(
            url,
            headers=headers,
            data=json.dumps(data)
        )
        res_json = res.json()
        return cls.from_data(data=res_json, client=client)
    
    def update(self, name=None):
        if name == None:
            raise Exception("Must Include Name in Collection Update")
        data = {
            "name": name
        }
        headers = {
            "Content-Type": "application/json",
            **self.client.headers  
        }
        res = requests.patch(
            self.url,
            headers=headers,
            data=json.dumps(data)
        )
        self._data = res.json()
        return self
    
        
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
        
    
    def filter(self,
            documents: List[str] = [],
            metadata: Any = {}
        ):
        from .Filter import Filter
        return Filter(documents=documents, collections=[self], metadata=metadata)

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
            include_docs: bool = False
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


    def get(self):
        self.load_state = 'loading'
        if self._id is not None:
            response = requests.get(
                self.url,
                headers=self.client.headers,
            )
        elif self._name is not None:
            response = requests.get(
                f'{self.client.workspace_api_url}/c/name/{self._name}', # TODO may need to serialize this?
                headers=self.client.headers,
            )

        if response.status_code == 200:
            data = response.json()
            self._data = data
            self._id = data['_id']
            self.load_state = 'loaded'
            return self
        else:
            self.load_state = 'error'
            raise NotFound("Collection")

    @property
    def url(self):
        return f'{self.client.workspace_api_url}/c/{self.id}'


    def upload(
            self,
            file: Optional[BufferedReader] = None,
            path: Optional[str] = None,
            name: Optional[str] = None,
            type: Optional[FileTypes] = 'auto',
            await_processed: Optional[bool] = True,
        ) -> Document:
        self.get_cache()
        url = f'{self.url}/upload'
        if file is not None:
            file_name = file.name.split('/')[-1]

        elif path is not None:
            file_obj = open(path, 'rb')
            file = file_obj.read()
            file_name = file_obj.name.split('/')[-1]

        mimetype, _ = mimetypes.guess_type(file_name)

        data = {
            'config': json.dumps({
                "name": name or file_name,
                # "docType":mimetypes.guess_type(file_name),
            }),
        }
        
        response = requests.post(
            url,
            headers=self.client.headers,
            data=data,
            files={'file' : (f'{file_name}', file, mimetype)},
        )
        
        doc = Document.from_data(response.json())
        

        if await_processed:
            doc.await_processed()
            
        return doc
    
    def document(self, id: str):
        from .Document import Document
        return Document(
            id=id,
            cid=self.id,
            client=self.client
        )
    

    @property
    def name(self) -> str:
        if self._name:
            return self._name
        return self.data['name']
    
    @property
    def state(self) -> str:
        return self.data['state']
    
    def __repr__(self):
        return self.__repr_nested__(indent=0)    

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)

        return f"""\
{self.__class__.__name__}(
{ind}id={self.id}
{ind}name={self.name}
{ind}docs={self.docs.__repr_nested__(indent+4)}
{" " * (indent)})"""