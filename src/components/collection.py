from src.models.node_type import NodeType
from src.models.base_node import BaseNode
from src.models.node import Node, FnLib, ExecFn, HOLib, HOExecFn

from src.internals.ghost import generate_ghost_id
from src.internals.registry import (
  register_fn,
  setup as setup_registry
)

fn_exports: list[ExecFn] = []
ho_exports: list[HOExecFn] = []
def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_registry(fn_lib, ho_lib, fn_exports, ho_exports)

@register_fn(fn_exports)
def collection(
  args: list[BaseNode],
  _: Node | None = None,
  fn_lib: FnLib = {},
) -> BaseNode:
  def fetch_fn(
    args_fn_args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    index: int = int(args_fn_args[0].fetch_float())
    if index < 0 or index >= len(args):
      return BaseNode()
    
    return args[index]

  ghost_id: str = generate_ghost_id()
  fn_lib[f"{ghost_id}:primary"] = fetch_fn

  return BaseNode(
    type=NodeType.GHOST,
    ghost_value=ghost_id,
  )

