from typing import TYPE_CHECKING

import requests
from ezllm import Client, Document
from ezllm.Entity import Entity
from ezllm.errors import NotFound
from ezllm.Document import Document
from ezllm.helpers import with_cache
if TYPE_CHECKING:
    from ezllm import Collection

class Documents(Entity):
    def __init__(self, collection: 'Collection', data=None, client: Client = None):
        super().__init__(id=None, data=data, client=client)
        self._docs = []
        self.collection = collection
        self.client = client or Client()

    
    @property
    def url(self):
        return f"{self.collection.url}/d"

    def format_data(self):
        self._docs = [Document.from_data(d) for d in self._data]

    @property
    @with_cache
    def docs(self):
        return self._docs

    def __len__(self):
        return len(self.docs)

    def __getitem__(self, index) -> Document:
        return self.docs[index]

    def __reversed__(self):
        return reversed(self.docs)
    
    def __iter__(self):
        return iter(self.docs)
    
    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)
        nested_repr = (' ' * (indent+8)) + ("\n" + (' ' * (indent+8))).join([obj.__repr_nested__(indent+8) for obj in self.docs])

        return f"""\
{self.__class__.__name__}(
{ind}docs=[
{nested_repr}
{ind}]
{" " * (indent)})"""