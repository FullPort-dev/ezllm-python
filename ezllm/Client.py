import os
import requests

from ezllm.constants import DEFAULT_API_URL, DEFAULT_RUN_URL


class SingletonMeta(type):
    # first client created, if key = None it returns this
    _default = None
    _instances = {}

    def __call__(cls, *args, **kwargs) -> 'Client':
        key = kwargs.get('key')
        if len(args) > 0:
            key = args[0]
        
        if key not in cls._instances:
            client = super(SingletonMeta, cls).__call__(*args, **kwargs)
            if len(cls._instances) == 0:
                cls._default = client
            
            cls._instances[key] = client
                
            if key == None:
                return cls._default
            
        return cls._instances[key]
    



class Client(metaclass=SingletonMeta):
    
    def __init__(self, key=None, secret=None,api_url=None,run_url=None):
        self.key = key or os.getenv('EZLLM_ACCESS_KEY')
        self.secret = secret or os.getenv('EZLLM_SECRET')
        self.api_url = api_url or os.getenv('EZLLM_API_URL') or DEFAULT_API_URL
        self.run_url = run_url or os.getenv('EZLLM_RUN_URL') or DEFAULT_RUN_URL
        # print('INIT CLIENT', self.key, self.secret, self.api_url, self.run_url)
        if self.key == None or self.secret == None:
            raise Exception("Please Provide a key and secret by passing it to Client() or adding to a .env https://docs.ezllm.io/quickstart")
        self.headers = {
            # "Content-Type": "application/json",
            'X-Access-Key' : self.key,
            'X-Access-Secret' : self.secret
        }
        self.loaded_data = self.load()
        # TODO throw error if cannot pull workspace

        if self.loaded_data:
            self.loaded_data = self.loaded_data.json()
            self.wid = self.loaded_data['workspaces'][0]['wid']
            self.workspace_api_url = f'{self.api_url}/w/{self.wid}'
            self.workspace_run_url = f'{self.run_url}/w/{self.wid}'
        else:
            print("[ERROR] loading workspace data")
            # raise Exception("Error loading workspace")

        
    def load(self):
        try:
            response = requests.get(
                f"{self.api_url}/user/me",
                headers=self.headers,
                timeout=60
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            try:
                print(f"Error: {response.json()}")
            except:
                print(f"Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"{err}")
        return response or None
        

    def Collection(self, id):
        from .Collection import Collection
        return Collection(id,client=self)
    
    def Collections(self):
        from .Collections import Collections
        return Collections(client=self)
    
    def __repr__(self):
        return self.__repr_nested__(indent=0)    

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)

        return f"""\
{self.__class__.__name__}(
{ind}key={self.key}
{ind}key={self.api_url}
{ind}key={self.run_url}
{" " * (indent)})"""

def get_default_client():
    return Client()


