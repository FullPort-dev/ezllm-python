from typing import Generic, TypeVar

from ezllm.response import MethodResponse

T = TypeVar('T', bound='MethodResponse')


class MethodBase(Generic[T]):
    def __init__(self, agg = 'accumulate') -> None:
        self.agg = agg
    
    def json(self):
        raise NotImplementedError()
    

    def format_response(self, data) -> T:
        raise NotImplementedError()