from typing import List
from ezllm.response import QAMethodResponse
from ezllm.methods.Base import MethodBase
from ezllm.types import LLMTypes


class QAMethod(MethodBase[QAMethodResponse]):
    def __init__(
            self,
            questions: List[str],
            agg = 'accumulate',
            llm: LLMTypes = 'gpt-3.5',
        ) -> None:
        super().__init__(agg, llm)
        self.questions = questions
    
    def json(self):
        return {
            "method" : {
                "type" : "qa",
                "aggregate" : {
                    "type" : self.agg
                },
                "metadata" : {                
                    "questions" : self.questions,
                },
                "llm_type" : self.llm,
            }
        }
    
    def format_response(self, data):
        return QAMethodResponse(data)