from src.models.node_type import NodeType
from src.models.base_node import BaseNode
from src.models.node import Node, FnLib, ExecFn, HOLib, HOExecFn

from src.internals.registry import (
  register_fn,
  setup as setup_registry
)

fn_exports: list[ExecFn] = []
ho_exports: list[HOExecFn] = []
def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_registry(fn_lib, ho_lib, fn_exports, ho_exports)

@register_fn(fn_exports)
def base(
  _: list[BaseNode],
  node: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  if (node is None): return BaseNode()
  if (node.value is None): return BaseNode()
  
  return node.value

@register_fn(fn_exports)
def endline(*_) -> BaseNode:
  return BaseNode(
    type=NodeType.STRING,
    str_value="\n"
  )

