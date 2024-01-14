from pandas import DataFrame
from ezllm.Documents import Document
from ezllm.methods import ExtractionMethod
from tests.constants import TEST_DOC_ID
from pydantic import BaseModel, Field
from typing import List

class PostModel(BaseModel):
    """extract the fields for each post"""
    post_title: str = Field(
        ...,
        description="name of the post"
    )
    upvotes: int = Field(
        ...,
        description="number of upvotes"
    )
    subreddit: str = Field(
        ...,
        description="Subreddit the post was from"
    )
    user: str = Field(
        ...,
        description="user who posted it"
    )

class ExtractModel(BaseModel):
    """extract data from text"""
    posts: List[PostModel] = Field(
        ...,
        description="list of posts extracted from provided text"
    )

def test_extraction():
    doc = Document(TEST_DOC_ID)
    method = ExtractionMethod(schema=ExtractModel)
    response = doc.run(method)
    print(response)
    
    posts = response.data[0]['posts']
    dfs = response.dfs
    df = dfs['posts']
    assert posts[2]['post_title'] == "[Serious] What's the scariest fact you wish you didn't know?"
    assert posts[0]['upvotes'] == 7792
    assert posts[-1]['user'] == "minerman30"

    assert type(dfs) == dict
    assert type(df) == DataFrame
    assert len(df) == 10

"""
No need to test doc.run() as it's just a wrapper around this
+ this operation isn't free
"""