from typing import List
from ezllm.response.Base import ResponseBase
from ezllm.response.DocOutputGroup import DocOutputGroups
from ezllm.response.ResponseDocs import ResponseDoc, ResponseDocs


class FilterResponse(ResponseBase[DocOutputGroups]):
    docs: ResponseDocs[ResponseDoc]
    pass