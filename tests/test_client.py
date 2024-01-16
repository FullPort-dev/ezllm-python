import os

import pytest
import ezllm
from ezllm import Client, Document

"""
THESE TESTS CAN'T BE RUN WITH OTHER TESTS BECAUSE IT SETS THE DEFAULT CLIENT TO AN INVALID ONE
"""
    
# def test_init_client_default():
#     c = Client(key='123', secret='456')
#     print("CLIENT", c)
#     assert c.key == '123'
#     c = Client()
#     assert c.key == '123'

#     doc = Document("")
#     print("", doc.client)
#     assert doc.client.key == '123'

# def test_env_init():
#     # to see if it resets between tests ?
#     # you 
#     """
    
    #I tried this
    
# import importlib

# @pytest.fixture(autouse=True)
# def reload_my_module():
#     importlib.reload(ezllm)
#     yield

#     """
#     c = ezllm.Client()
#     print(c)
#     assert c.key == os.getenv('EZLLM_ACCESS_KEY')