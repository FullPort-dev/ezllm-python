import json
from typing import Generic, List, Optional, TypeVar


T = TypeVar('T', bound='OutputGroup')
D = TypeVar('D', bound='OutputData')
DT = TypeVar('DT')

class OutputData(Generic[DT]):
    def __init__(self, data: DT):
        self.data: DT = data


    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0) -> str:
        ind = ' ' * (indent+4)
        data_str = json.dumps(self.data, indent=4)
        data_str = ("\n" + ind).join(data_str.splitlines())

        return f"""\
{self.__class__.__name__}(
{ind}data={data_str}
{' ' * (indent)})"""
        
class OutputGroup(Generic[D]):
    OutputDataClass: D = OutputData

    def __init__(self, group):
        self._data: D = self.OutputDataClass(group['output'])
        self.type = group['type']
        self.id: Optional[str] = group['id']

    @property
    def data(self):
        # print("YO123", self._data.data)
        return self._data.data

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0) -> str:
        ind = ' ' * (indent+4)
        return f"""\
{self.__class__.__name__}(
{ind}type={self.type}
{ind}id={self.id}
{ind}output={self._data.__repr_nested__(indent+4)}
{' ' * (indent)})"""


        

class OutputGroups(Generic[T]):
    OutputGroupClass: T = OutputGroup
    def __init__(self, data):
        self.groups: List[T] = [self.OutputGroupClass(g) for g in data]
        
    @property
    def data(self):
        output = []
        for group in self.groups:
            output.extend(group.data)
        return output
        
    
    def by_id(self, id: str) -> T:
        for group in self.groups:
            if group.id == id:
                return group
        return None  # or some default value if no group is found


    def __len__(self):
        return len(self.groups)

    def __getitem__(self, index) -> T:
        return self.groups[index]

    def __reversed__(self):
        return reversed(self.groups)
    
    def __iter__(self):
        return iter(self.groups)
    
    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent+4)
        nested_repr = (' ' * (indent+8)) + ("\n" + (' ' * (indent+8))).join([obj.__repr_nested__(indent+8) for obj in self.groups])

        return f"""\
{self.__class__.__name__}(
{ind}groups=[
{nested_repr}
{ind}]
{" " * (indent)})"""