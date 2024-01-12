from collections import defaultdict
from typing import Any, Dict, List
from ezllm.response.Base import MethodResponse
from ezllm.response.OutputGroup import OutputData, OutputGroups, OutputGroup


class ExtractionOutputData(OutputData[Dict]):
    pass

class ExtractionOutputGroup(OutputGroup[ExtractionOutputData]):
    data: Dict
    OutputDataClass = ExtractionOutputData

class ExtractionOutputGroups(OutputGroups[ExtractionOutputGroup]):
    OutputGroupClass = ExtractionOutputGroup
    @property
    def data(self) -> List[Dict]:
        return [group.data for group in self.groups]

class ExtractionMethodResponse(MethodResponse[ExtractionOutputGroups, Any]):
    # data: List[ExtractionOutputData]
    OutputGroupsClass = ExtractionOutputGroups

    @property
    def df(self):
        import pandas as pd
        out = defaultdict(list)
        data = self.output.data
        
        if list not in [type(x) for x in data[0].values()]:
            raise Exception("Output type must include a list to be formatted as a df")

        for output_group in data:
            for key, value in output_group.items():
                if type(value) == list:
                    out[key].extend(value)

        if len(out) == 1:
            return pd.DataFrame(list(out.values())[0])
        else:
            raise Exception("")

    @property
    def dfs(self):
        import pandas as pd
        out = defaultdict(list)
        data = self.output.data

        if list not in [type(x) for x in data[0].values()]:
            raise Exception("Output type must include a list to be formatted as a df")

        for output_group in data:
            for key, value in output_group.items():
                if type(value) == list:
                    # TODO : throw error if no lists provide, i.e it's a single datum extraction
                    out[key].extend(value)

        df_dict: Dict[str, pd.DataFrame] = {}
        for key, value in out.items():
            df_dict[key] = pd.DataFrame(value)
        
        return df_dict