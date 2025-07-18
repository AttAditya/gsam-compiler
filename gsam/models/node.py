from __future__ import annotations
from typing import Self, TypeAlias, Callable

from gsam.models.node_type import NodeType
from gsam.models.base_node import BaseNode
from gsam.models.node_signal import NodeSignal

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

  def clone(self: Self) -> Node:
    return Node(
      executes=self.executes,
      script=self.script.clone() if self.script else None,
      value=self.value.clone() if self.value else None,
      next_node=self.next if self.next else None,
      high_order=self.high_order,
    )

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
    if self.high_order:
      next_node = self.high_order_execute(fn_lib, ho_lib)
      if next_node is None: return BaseNode(), self.next
      return next_node.execute(
        fn_lib,
        ho_lib
      )

    current: Node | None = self.script
    args: list[BaseNode] = []
    result: BaseNode = BaseNode()

    while current is not None:
      value, next_node = current.execute(fn_lib, ho_lib)
      args.append(value)

      if value.signal == NodeSignal.RETURN:
        result = value
        next_node = None

      current = next_node

    if self.executes is None:
      return result, self.next
    
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
