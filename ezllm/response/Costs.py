from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class ResponseCost:
    cost: int
    date: datetime
    step: str
    usage: int
    limitType: str
    limitId: str
    desc: Optional[str] = None
    reportedCost: Optional[float] = None
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * indent
        return f'{ind}{self.__repr__()}'

class ResponseCosts:
    def __init__(self, data, total_cost):
        self.data = data
        self.costs = [ResponseCost(**c) for c in data]
        self.total_cost: int = total_cost



    def __len__(self):
        return len(self.costs)

    def __iter__(self):
        return iter(self.costs)
    
    def __getitem__(self, index: int) -> ResponseCost:
        return self.costs[index]

    def __repr__(self):
        return self.__repr_nested__(indent=0)
    
    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent + 4)

        nested_repr = ind + ("\n" + ind).join([obj.__repr_nested__(indent) for obj in self.costs])

        return f"""\
{self.__class__.__name__}(
{ind}total_cost={self.total_cost},
{ind}costs=[
{nested_repr}
{ind}]
{" " * indent})"""