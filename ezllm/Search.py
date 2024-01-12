from typing import List, overload
from ezllm.response import SearchResponse
from ezllm.Retrieval import RetrievalBase
from ezllm.response.ResponseDocs import SearchResponseDoc
from .Client import Client
from .Filter import Filter

class SearchRetrieval(RetrievalBase[SearchResponse]):
    ResponseClass = SearchResponse
    def __init__(
            self,
            query,
            client: Client,
            filter: Filter  = None,
            n_docs = 10,
            group='all'
        ):
        super().__init__(client, filter, group)
        self.query = query
        self.n = n_docs
    
    def json(self):
        return {
            **self.filter.json(),
            "retrieval": {
                "type": 'search',
                'accumulate' : {
                    "type" : self.group
                },
                "metadata": {
                    "query":self.query,
                    "n":self.n
                }
            }
        }
    

    def get(self) -> SearchResponse:
        return super().get()
    
    @property
    def docs(self) -> List[SearchResponseDoc]:
        self.get_cache()
        return self.output.docs