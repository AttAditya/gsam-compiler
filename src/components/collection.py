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
  ghost_id: str = generate_ghost_id()
  
  def fetch_fn(
    args_fn_args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    if len(args_fn_args) == 0:
      return BaseNode(
        type=NodeType.GHOST,
        ghost_value=ghost_id,
      )
    
    index: int = int(args_fn_args[0].fetch_float())
    if index < 0 or index >= len(args):
      return BaseNode()
    
    return args[index]
  
  def push_fn(
    args_fn_args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    if len(args_fn_args) == 0:
      args_fn_args.append(BaseNode())
    
    value: BaseNode = args_fn_args[0]
    if len(args_fn_args) == 1:
      args.append(value)
      return BaseNode(
        type=NodeType.BOOLEAN,
        bool_value=True,
      )
    
    index: int = int(args_fn_args[1].fetch_float())
    if index < 0 or index >= len(args):
      return BaseNode(
        type=NodeType.BOOLEAN,
        bool_value=False,
      )
    
    args.insert(index, value)
    
    return BaseNode(
      type=NodeType.BOOLEAN,
      bool_value=True
    )

  fn_lib[f"{ghost_id}:primary"] = fetch_fn
  fn_lib[f"{ghost_id}:push"] = push_fn

  return BaseNode(
    type=NodeType.GHOST,
    ghost_value=ghost_id,
  )

@register_fn(fn_exports)
def push(
  args: list[BaseNode],
  _: Node | None = None,
  fn_lib: FnLib = {},
) -> BaseNode:
  if len(args) == 0:
    return BaseNode(
      type=NodeType.BOOLEAN,
      bool_value=False
    )

  collection_arg = args[0]
  ghost_value: str | None = collection_arg.ghost_value
  if ghost_value is None:
    return BaseNode(
      type=NodeType.BOOLEAN,
      bool_value=False
    )
  
  push_fn: ExecFn | None = fn_lib.get(f"{ghost_value}:push")
  if push_fn is None:
    return BaseNode(
      type=NodeType.BOOLEAN,
      bool_value=False
    )
  
  push_value: BaseNode = BaseNode()
  if len(args) == 2:
    push_value = args[1]

  push_index: int | None = None
  if len(args) > 2:
    push_index = int(args[2].fetch_float())
    if push_index < 0 or push_index >= len(args):
      return BaseNode(
        type=NodeType.BOOLEAN,
        bool_value=False
      )
  
  fn_args: list[BaseNode] = [push_value]
  if push_index is not None:
    fn_args.append(BaseNode(
      type=NodeType.NUMERIC,
      float_value=float(push_index)
    ))
  
  push_fn(fn_args, None, fn_lib)
  return BaseNode(
    type=NodeType.BOOLEAN,
    bool_value=True
  )

