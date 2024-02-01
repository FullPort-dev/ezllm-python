from typing import Dict
import requests

from ezllm import Client
from ezllm.errors import NotFound, handle_request_errors
from ezllm.helpers import with_cache


class Entity:
    def __init__(
            self,
            id: str = None,
            data: Dict = None,
            client: Client = None
        ):
        self.load_state = 'unloaded'
        self._data: Dict = data or {}
        self._id = id or self._data.get('_id')
        self.client = client or Client()

    @property
    def url(self):
        raise NotImplementedError()

    def format_data(self):
        pass

    def get(self):
        self.load_state = 'loading'
        res = requests.get(
            self.url,
            headers=self.client.headers,
        )
        handle_request_errors(res)

        if res.status_code == 200:
            # TODO format this into a Document
            data = res.json()
            if type(data) == dict:
                self._id = data.get('_id')
            self._data = data
            # TODO should this return self or a new instance?
            self.load_state = 'loaded'
            self.format_data()
            return self
        else:
            self.load_state = 'error'
            print("ERROR FETCHING", res.status_code)
            raise NotFound("")
    
    def get_cache(self):
        if self.load_state == 'loaded':
            return self._data

        self.get()
        return self._data


    @classmethod
    def from_data(cls, data, client: Client = None):
        return cls(
            data=data,
            client=client,
        )
    
    @property
    @with_cache
    def data(self):
        return self._data
    

    @property
    def id(self) -> str:
        if self._id:
            return self._id
        data = self.get_cache()
        return data['_id']