from .Client import Client
from .Collection import Collection
import requests

class Collections:
    def __init__(self,client:Client):
        self.client = client
        
        res = requests.get(
                f'{self.client.workspace_api_url}/collections',
                headers=self.client.headers,
            )
        self.collections = []
        
        if res.status_code == 200:
            res = res.json()
            for i in res:
                self.collections.append(
                    Collection(id=i['_id'],client=self.client)
                )

        
    
    def __iter__(self):
        return iter(self.collections)