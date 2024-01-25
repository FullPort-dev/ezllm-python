from typing import List
from ezllm.response import QAMethodResponse
from ezllm.methods.Base import MethodBase


class QAMethod(MethodBase[QAMethodResponse]):
    def __init__(self, questions: List[str], agg = 'accumulate') -> None:
        super().__init__(agg)
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