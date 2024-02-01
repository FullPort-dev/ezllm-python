from typing import Generic, TypeVar

from ezllm.response import MethodResponse
from ezllm.types import AggTypes, LLMTypes

T = TypeVar('T', bound='MethodResponse')


class MethodBase(Generic[T]):
    def __init__(
            self,
            agg: AggTypes = 'accumulate',
            llm: LLMTypes = 'gpt-3.5',
        ) -> None:
        self.agg = agg
        self.llm = llm
    
    def json(self):
        raise NotImplementedError()
    

    def format_response(self, data) -> T:
        raise NotImplementedError()