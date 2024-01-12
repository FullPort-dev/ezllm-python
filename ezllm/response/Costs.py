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
    

class ResponseCosts:
    def __init__(self, data, total_cost):
        self.data = data
        self.costs = [ResponseCost(**c) for c in data]
        self.total_cost: int = total_cost

    def __repr__(self, indent=8):
        ind = ' ' * indent

        nested_repr = (' '*(indent+4)) + ("\n" + (' '*(indent+4))).join([repr(obj) for obj in self.costs])

        return f"""\
{self.__class__.__name__}(
{ind}total_cost={self.total_cost},
{ind}costs=[
{nested_repr}
{ind}]
{" " * 4})"""