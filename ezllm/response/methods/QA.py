from ezllm.response.Base import MethodResponse


class QAMethodResponse(MethodResponse):
    pass


from typing import Any, Dict, List
from ezllm.response.Base import MethodResponse
from ezllm.response.OutputGroup import OutputData, OutputGroups, OutputGroup


class QAOutputDatum:
    def __init__(self, data):
        self.question = data['question']
        self.answer = data['answer']
        self.relevant: int = data['relevant']

class QAOutputData(OutputData[Any]):
    def __init__(self, data):
        self.data = data
        self.questions = [QAOutputDatum(d) for d in self.data]

class QAOutputGroup(OutputGroup[QAOutputData]):
    data: List[Dict]
    OutputDataClass = QAOutputData

    @property
    def questions(self):
        return self._data.questions
    
    

class QAOutputGroups(OutputGroups[QAOutputGroup]):
    OutputGroupClass = QAOutputGroup
    @property
    def data(self):
        output = []
        for group in self.groups:
            output.extend(group.data)
        return output
        # return [group.data for group in self.groups]

class QAMethodResponse(MethodResponse[QAOutputGroups, QAOutputDatum]):
    data: List[QAOutputDatum]
    # data: List[ExtractionOutputData]
    OutputGroupsClass = QAOutputGroups
