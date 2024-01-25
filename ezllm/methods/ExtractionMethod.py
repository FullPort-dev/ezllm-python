from typing import Type
from pydantic import BaseModel
from ezllm.methods.Base import MethodBase
from ezllm.response import ExtractionMethodResponse
from ezllm.types import AggTypes, LLMTypes




class ExtractionMethod(MethodBase[ExtractionMethodResponse]):
    def __init__(
            self,
            schema: Type[BaseModel],
            agg: AggTypes = 'accumulate',
            llm: LLMTypes = 'gpt-3.5',
        ) -> None:
        super().__init__(agg, llm)
        self.schema = schema
    
    def json(self):
        json_schema = self.schema.schema()
        return {
            "method" : {
                "type" : "extract",
                "aggregate" : {
                    "type" : self.agg
                },
                "metadata" : {                
                    "extract_schema" : json_schema,
                },
                "llm_type" : self.llm,
            }
        }
    
    def format_response(self, data):
        return ExtractionMethodResponse(data)
