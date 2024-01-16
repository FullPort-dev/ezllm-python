from ezllm.types import GroupTypes
from .Document import Document
from .Collection import Collection
from .Client import Client
from ezllm.response import FilterResponse, ResponseDoc

import json
import requests
from typing import List, Union



class Filter:
    def __init__(self,
            documents: List[Union[Document, str]] = [],
            collections: List[Union[Collection,str]] = [],
            metadata = {}, # TODO add typing
            client: Client = None
        ):
        self.documents = documents
        self.collections = collections
        self.metadata = metadata
        self.client = client or Client()
        self.data = None
        self._output = None
        

    def get_ids(self, list):
        out = []
        for i in list:
            if type(i) == str:
                out.append(i)
            else:
                out.append(i.id)
        return out
    
    def create_metadata(self):
        out = {}
        for key, value in self.metadata.items():
            value_type = type(value)
            if value_type != dict and value_type != tuple and value_type != list:
                out[key] = {'eq' : value}
                
            # TODO add handling for lt, lte ... 

        return out
    
    def json(self):
        return {
        "filter" : {
            "collections" : self.get_ids(self.collections),
            "documents" : self.get_ids(self.documents),
            "subdocs" : [],
            "metadata" : self.create_metadata()
        }}

    def scan(
            self,
            group: GroupTypes = 'all',
        ):
        from .Scan import ScanRetrieval
        return ScanRetrieval(
            client=self.client,
            filter=self,
            group=group
        )

    
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
            filter=self,
            group=group,
        )
        
    def get(self):
        url = f"{self.client.workspace_run_url}/filter"
        body = json.dumps(
            self.json()
        )
        response = requests.post(url, data=body, headers=self.client.headers)
        
        
        if response.status_code == 200:
            data= response.json()
            self.data = data
            self._output = FilterResponse(data)
            return self._output
        
        else:
            print("Error: ", response.status_code)

    
    def get_cache(self):
        if self.data == None:
            self.get()
        
        return self.data
    
    @property
    def docs(self) -> List[ResponseDoc]:
        self.get_cache()
        return self._output.docs
    
    @property
    def output(self) -> FilterResponse:
        self.get_cache()
        return self._output

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)

        # TODO : serialize json nicer
        return f"""\
{self.__class__.__name__}(
{ind}output={self._output.__repr_nested__(indent+4) if self.output else None}
{ind}filter={json.dumps(self.json()['filter'], indent=indent+8)}
{" " * (indent)})"""