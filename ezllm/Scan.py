from enum import Enum
from typing import List, overload
from ezllm.response import ScanResponse, ResponseDoc
from ezllm.Retrieval import RetrievalBase
from ezllm.types import GroupTypes
from .Client import Client
from .Filter import Filter




class ScanRetrieval(RetrievalBase[ScanResponse]):
    ResponseClass = ScanResponse
    def __init__(
        self,
        client: Client = None,
        filter: Filter  = None,
        group: GroupTypes = 'all',
    ):
        super().__init__(client, filter, group)
    

    def get(self) -> ScanResponse:
        return super().get()

    @property
    def docs(self) -> List[ResponseDoc]:
        self.get_cache()
        return self.output.docs
    
    def json(self):
        return {
            **self.filter.json(),
                "retrieval": {
                    "type": 'scan',
                    'accumulate' : {
                        "type" : self.group
                    },
                    "metadata": {

                    }
                }
        }