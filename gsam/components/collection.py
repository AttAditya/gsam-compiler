from gsam.models.node_type import NodeType
from gsam.models.base_node import BaseNode
from gsam.models.node import Node, FnLib, ExecFn, HOLib, HOExecFn

from gsam.internals.ghost import generate_ghost_id
from gsam.internals.registry import (
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
    fn_args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    if len(fn_args) == 0:
      return BaseNode(
        type=NodeType.GHOST,
        ghost_value=ghost_id,
      )
    
    index: int = int(fn_args[0].fetch_float())
    if index < 0 or index >= len(args):
      return BaseNode()
    
    return args[index]
  
  def push_fn(
    fn_args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    if len(fn_args) == 0:
      fn_args.append(BaseNode())
    
    value: BaseNode = fn_args[0]
    if len(fn_args) == 1:
      args.append(value)
      return BaseNode(
        type=NodeType.BOOLEAN,
        bool_value=True,
      )
    
    index: int = int(fn_args[1].fetch_float())
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

  def update_fn(
    fn_args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    value: BaseNode = fn_args[0]
    index: int = int(fn_args[1].fetch_float())

    if index < 0 or index >= len(args):
      return BaseNode(
        type=NodeType.BOOLEAN,
        bool_value=False,
      )
    
    args[index] = value
    return BaseNode(
      type=NodeType.BOOLEAN,
      bool_value=True
    )

  def pop_fn(
    fn_args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    fn_args.append(BaseNode(
      type=NodeType.NUMERIC,
      float_value=len(args) - 1
    ))

    index: int = int(fn_args[0].fetch_float())
    if index < 0 or index >= len(args):
      return BaseNode()
    
    result = args.pop(index)
    return result
  
  def size_fn(*_) -> BaseNode:
    return BaseNode(
      type=NodeType.NUMERIC,
      float_value=float(len(args))
    )

  fn_lib[f"{ghost_id}:primary"] = fetch_fn
  fn_lib[f"{ghost_id}:push"] = push_fn
  fn_lib[f"{ghost_id}:pop"] = pop_fn
  fn_lib[f"{ghost_id}:update"] = update_fn
  fn_lib[f"{ghost_id}:size"] = size_fn

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
  
  fn_args: list[BaseNode] = [push_value]
  if push_index is not None:
    fn_args.append(BaseNode(
      type=NodeType.NUMERIC,
      float_value=float(push_index)
    ))
  
  return push_fn(fn_args, None, fn_lib)

@register_fn(fn_exports)
def pop(
  args: list[BaseNode],
  _: Node | None = None,
  fn_lib: FnLib = {},
) -> BaseNode:
  if len(args) == 0: return BaseNode()

  collection_arg = args[0]
  ghost_value: str | None = collection_arg.ghost_value
  if ghost_value is None: return BaseNode()
  
  pop_fn: ExecFn | None = fn_lib.get(f"{ghost_value}:pop")
  if pop_fn is None: return BaseNode()
  
  push_index: int | None = None
  if len(args) > 1:
    push_index = int(args[1].fetch_float())
  
  fn_args: list[BaseNode] = []
  if push_index is not None:
    fn_args.append(BaseNode(
      type=NodeType.NUMERIC,
      float_value=float(push_index)
    ))
  
  return pop_fn(fn_args, None, fn_lib)

@register_fn(fn_exports)
def update(
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
  
  update_fn: ExecFn | None = fn_lib.get(f"{ghost_value}:update")
  if update_fn is None:
    return BaseNode(
      type=NodeType.BOOLEAN,
      bool_value=False
    )
  
  if len(args) < 3:
    return BaseNode(
      type=NodeType.BOOLEAN,
      bool_value=False
    )
  
  update_value = args[1]
  push_index = int(args[2].fetch_float())
  fn_args: list[BaseNode] = [
    update_value, BaseNode(
      type=NodeType.NUMERIC,
      float_value=float(push_index)
    )
  ]
  
  return update_fn(fn_args, None, fn_lib)

@register_fn(fn_exports)
def size(
  args: list[BaseNode],
  _: Node | None = None,
  fn_lib: FnLib = {},
) -> BaseNode:
  if len(args) == 0: return BaseNode()

  collection_arg = args[0]
  ghost_value: str | None = collection_arg.ghost_value
  if ghost_value is None: return BaseNode()
  
  size_fn: ExecFn | None = fn_lib.get(f"{ghost_value}:size")
  if size_fn is None: return BaseNode()
  return size_fn([], None, fn_lib)

