from typing import Self

from .node_type import NodeType

class BaseNode:
  type: str
  base: bool
  str_value: str | None
  float_value: float | None
  bool_value: bool | None
  ghost_value: str | None = None
  signal: str | None = None

  def __init__(
    self: Self,
    base: bool = True,
    type: str = NodeType.VOID,
    str_value: str | None = None,
    float_value: float | None = None,
    bool_value: bool | None = None,
    ghost_value: str | None = None,
    signal: str | None = None,
  ) -> None:
    self.base = base
    self.type = type
    self.signal = signal

    self.str_value = str_value
    self.float_value = float_value
    self.bool_value = bool_value

    self.ghost_value = ghost_value

  def fetch_str(self: Self) -> str:
    if self.type == NodeType.NUMERIC:
      return str(self.fetch_float())
    
    if self.type == NodeType.BOOLEAN:
      return 'true' if self.fetch_bool() else 'false'
    
    if self.str_value is None:
      return ""
    
    return self.str_value

  def fetch_float(self: Self) -> float:
    if self.type == NodeType.BOOLEAN:
      return 1.0 if self.fetch_bool() else 0.0
    
    if self.type == NodeType.TEXT:
      try:
        return float(self.fetch_str())
      except ValueError:
        return 0.0
      
    if self.float_value is None:
      return 0.0
    
    return self.float_value
  
  def fetch_bool(self: Self) -> bool:
    if self.type == NodeType.NUMERIC:
      return self.fetch_float() != 0.0
    
    if self.type == NodeType.TEXT:
      return len(self.fetch_str()) != 0
    
    if self.bool_value is None:
      return False
    
    return self.bool_value

