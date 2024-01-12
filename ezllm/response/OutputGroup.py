import json
from typing import Generic, List, Optional, TypeVar


T = TypeVar('T', bound='OutputGroup')
D = TypeVar('D', bound='OutputData')
DT = TypeVar('DT')

class OutputData(Generic[DT]):
    def __init__(self, data: DT):
        self.data: DT = data

    def __repr__(self, indent=20) -> str:
        ind = ' ' * indent
        data_str = json.dumps(self.data, indent=4)
        data_str = ("\n" + ind).join(data_str.splitlines())

        return f"""\
{self.__class__.__name__}(
{ind}data={data_str}
{' ' * (indent-4)})"""
        
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

    def __repr__(self, indent=16) -> str:
        ind = ' ' * indent
        return f"""\
{self.__class__.__name__}(
{ind}type={self.type}
{ind}id={self.id}
{ind}output={self._data}
{' ' * (indent-4)})"""


        

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
    

    def __repr__(self, indent=8):
        ind = ' ' * indent
        nested_repr = (' ' * (indent + 4)) + ("\n" + (' ' * (indent+4))).join([repr(obj) for obj in self.groups])

        return f"""\
{self.__class__.__name__}(
{ind}groups=[
{nested_repr}
{ind}]
{" " * (indent-4)})"""