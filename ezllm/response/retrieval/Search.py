from ezllm.response.DocOutputGroup import SearchDocOutputGroups
from ezllm.response.ResponseDocs import SearchResponseDocs
from ezllm.response.Base import ResponseBase


class SearchResponse(ResponseBase):
    DocGroupClass = SearchDocOutputGroups
    docs: SearchResponseDocs