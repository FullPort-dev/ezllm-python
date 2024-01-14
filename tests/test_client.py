import os
from ezllm import Client

def test_init_client_default():
    c = Client(key='123', secret='456')
    print("CLIENT", c)
    assert c.key == '123'
    c = Client()
    assert c.key == '123'

def test_env_init():
    # to see if it resets between tests ?
    c = Client()
    print(c)
    assert c.key == os.getenv('EZLLM_ACCESS_KEY')