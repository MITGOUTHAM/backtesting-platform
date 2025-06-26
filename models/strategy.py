from pydantic import BaseModel
from typing import List

class StrategyRequest(BaseModel):
  symbol : str
  interval : str
  capital : float
  indicators : List[str]
  