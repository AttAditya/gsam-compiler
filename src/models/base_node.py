from typing import Self
from .node_type import NodeType

class BaseNode:
  type: str
  base: bool
  str_value: str | None
  float_value: float | None
  bool_value: bool | None

  def __init__(
    self: Self,
    base: bool = True,
    type: str = NodeType.VOID,
    str_value: str | None = None,
    float_value: float | None = None,
    bool_value: bool | None = None,
  ) -> None:
    self.base = base
    self.type = type

    self.str_value = str_value
    self.float_value = float_value
    self.bool_value = bool_value

  def fetch_str(self: Self) -> str:
    if self.str_value is None:
      if self.float_value is not None:
        return str(self.float_value)
        
      return 'true' if self.bool_value else 'false'
    
    return self.str_value

  def fetch_float(self: Self) -> float:
    if self.float_value is None:
      if self.bool_value is not None:
        return 1.0 if self.bool_value else 0.0
      
      return 0.0
    
    return self.float_value
  
  def fetch_bool(self: Self) -> bool:
    if self.bool_value is None:
      if self.float_value is not None:
        return self.float_value != 0.0
      
      return not not self.str_value
    
    return self.bool_value

