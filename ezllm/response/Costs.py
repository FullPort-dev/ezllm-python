from dataclasses import dataclass
import datetime
from typing import Optional


def format_cost(cost: int):
    """
    formats the cost to be human readable
    """

    return f'${cost / 1000}'

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
    
    _formatted_cost: str = None  # Add an attribute for the formatted cost

    def __post_init__(self):
        # Format the cost after initialization
        self._formatted_cost = format_cost(self.cost)

    def __repr_nested__(self, indent=0):
        ind = ' ' * indent
        return f'{ind}{self.__repr__()}'
    

    def __repr__(self):
        return self.__repr_nested__(indent=0)

    def __repr_nested__(self, indent=0):
        ind = ' ' * (indent + 4)
        return f"""\
{self.__class__.__name__}(
{ind}cost={self._formatted_cost}
{ind}date={self.date!r}
{ind}step={self.step!r}
{ind}usage={self.usage}
{ind}limitType={self.limitType!r}
{ind}limitId={self.limitId!r}
{ind}desc={self.desc!r}
{ind}reportedCost={self.reportedCost!r}
{" " * indent})"""



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
        nested_ind = ' ' * (indent+8)

        # nested_repr = ind + ("\n" + ind).join([obj.__repr_nested__(indent) for obj in self.costs])
        nested_repr = f'[\n{nested_ind}{(nested_ind).join([obj.__repr_nested__(indent+8) for obj in self.costs])}\n{ind}]'

        return f"""\
{self.__class__.__name__}(
{ind}total_cost={format_cost(self.total_cost)},
{ind}costs={nested_repr}
{" " * indent})"""