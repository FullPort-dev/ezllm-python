from enum import Enum
from io import BufferedReader
import time
from typing import Any, List, Optional
from ezllm.Documents import Document
from ezllm.constants import UPLOAD_TIMEOUT
from ezllm.errors import FileProcessingError, NotFound
from ezllm.types import GroupTypes
from .Client import Client
import mimetypes
import json
import requests

class FileTypes(Enum):
    pdf='pdf'
    csv='csv'
    txt='txt'

class Collection():
    def __init__(
            self,
            id=None,
            name=None,
            client:Client=None
        ):
        self._name = name
        self._id = id
        self.client = client or Client()
        self.data = None
    
    
    @classmethod
    def create(cls, name, client: Client = None):
        client = client or Client()
        url = f'{client.workspace_api_url}/c/'
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
        return Collection(
            id=res_json['_id'],
            name=res_json['name'],
            client=client,
        )
    
    
    
    def update(self, name):
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
        self.data = res.json()
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
        self.data = res.json()
        return self
        
    
    def collection(self, *args, **kwargs):
        return Collection(*args, client=self, **kwargs)   
    
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

    
    def get(self):
        if self._id is not None:
            response = requests.get(
                f'{self.client.workspace_api_url}/c/{self._id}',
                headers=self.client.headers,
            )
        elif self._name is not None:
            response = requests.get(
                f'{self.client.workspace_api_url}/c/name/{self._name}', # TODO may need to serialize this?
                headers=self.client.headers,
            )

        if response.status_code == 200:
            data = response.json()
            self.data = data
            self._id = data['_id']
            return data
        else:
            raise NotFound("Collection")

    def get_cache(self):
        if self.data == None:
            self.get()
        
        return self.data

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
        
        doc = Document(data=response.json())
        

        if await_processed:
            doc.await_processed()
            
        return doc
    
    def document(self,id):
        from .Documents import Document
        return Document(id=id,cid=self.id,client=self.client)
    

    @property
    def name(self) -> str:
        if self.name:
            return self.name
        data = self.get_cache()
        return data['name']
    
    @property
    def id(self) -> str:
        if self._id:
            return self._id
        data = self.get_cache()
        return data['_id']
    
    @property
    def state(self) -> str:
        data = self.get_cache()
        return data['state']