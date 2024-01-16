from typing import List
from ezllm.Entity import Entity
from ezllm.helpers import with_cache
from .Client import Client
from .Collection import Collection
import requests

class Collections(Entity):
    def __init__(self, data=None, client: Client = None):
        super().__init__(id=None, data=data, client=client)
        self.state = 'unloaded'
        self._collections: List[Collection] = []
    

    def format_data(self):
        for i in self.data:
            self._collections.append(Collection.from_data(data=i, client=self.client))

    @property
    @with_cache
    def collections(self):
        return self._collections

    @property
    def url(self):
        return f'{self.client.workspace_api_url}/c'
        
    def __len__(self):
        return len(self.collections)

    def __iter__(self):
        return iter(self.collections)

    def __reversed__(self):
        return reversed(self.collections)
        
    def __getitem__(self, index: int) -> Collection:
        return self.collections[index]
    
    def __repr__(self):
        return self.__repr_nested__(indent=0)    

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)
        nested_repr = (' ' * (indent+8)) + ("\n" + (' ' * (indent+8))).join([obj.__repr_nested__(indent+8) for obj in self.collections])

        return f"""\
{self.__class__.__name__}(
{ind}collections=[
{nested_repr}
]
{" " * (indent)})"""