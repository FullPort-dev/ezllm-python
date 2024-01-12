from typing import List
from ezllm.response.Base import ResponseBase
from ezllm.response.ResponseDocs import ResponseDocs, ResponseDoc


class ScanResponse(ResponseBase[ResponseDoc]):
    docs: ResponseDocs[ResponseDoc]
    pass