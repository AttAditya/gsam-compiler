from __future__ import annotations
from typing import Self, TypeAlias, Callable

from .node_type import NodeType
from .base_node import BaseNode

class Node(BaseNode):
  executes: str | None
  script: Node | None
  value: BaseNode | None = None
  next: Node | None = None
  high_order: bool = False

  def __init__(
    self: Self,
    executes: str | None = None,
    script: Node | None = None,
    value: BaseNode | None = None,
    next_node: Node | None = None,
    high_order: bool = False,
  ) -> None:
    super().__init__(
      type=NodeType.NODE,
      base=False,
    )

    self.executes = executes
    self.script = script
    self.value = value
    self.next = next_node
    self.high_order = high_order

  def high_order_execute(
    self: Self,
    fn_lib: FnLib,
    ho_lib: HOLib,
  ) -> Node | None:
    if self.executes is None: return None
    if self.executes not in ho_lib: return None

    return ho_lib[self.executes](
      self,
      fn_lib,
      ho_lib,
    )

  def execute(
    self: Self,
    fn_lib: FnLib,
    ho_lib: HOLib,
  ) -> tuple[BaseNode, Node | None]:
    current: Node | None = self.script
    args: list[BaseNode] = []

    while current is not None:
      next_node = None

      if not current.high_order:
        value, next_node = current.execute(fn_lib, ho_lib)
        args.append(value)
      else:
        next_node = current.high_order_execute(fn_lib, ho_lib)
      
      current = next_node

    result: BaseNode = BaseNode()
    if self.executes is not None:
      result = fn_lib[self.executes](
        args,
        self,
        fn_lib
      )

    return result, self.next

ExecFn: TypeAlias = Callable[
  [
    list[BaseNode],
    Node | None,
    dict[str, "ExecFn"]
  ],
  BaseNode
]

HOExecFn: TypeAlias = Callable[
  [
    Node,
    dict[str, ExecFn],
    dict[str, "HOExecFn"]
  ],
  Node | None
]

FnLib: TypeAlias = dict[str, ExecFn]
HOLib: TypeAlias = dict[str, HOExecFn]
