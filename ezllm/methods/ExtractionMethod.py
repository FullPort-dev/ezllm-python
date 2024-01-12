from pydantic import BaseModel
from ezllm.methods.Base import MethodBase
from ezllm.response import ExtractionMethodResponse




class ExtractionMethod(MethodBase[ExtractionMethodResponse]):
    def __init__(self, schema: BaseModel, agg = 'accumulate') -> None:
        super().__init__(agg)
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
                }
            }
        }
    
    def format_response(self, data):
        return ExtractionMethodResponse(data)
