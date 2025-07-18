from gsam.models.node_type import NodeType
from gsam.models.node_signal import NodeSignal
from gsam.models.base_node import BaseNode
from gsam.models.node import Node, FnLib, ExecFn, HOLib, HOExecFn

from gsam.internals.registry import (
  register_fn,
  register_ho,
  setup as setup_registry
)

from .collection import collection

fn_exports: list[ExecFn] = []
ho_exports: list[HOExecFn] = []
def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_registry(fn_lib, ho_lib, fn_exports, ho_exports)

@register_fn(fn_exports)
def script(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  for arg in args:
    if arg.signal == NodeSignal.RETURN:
      return arg
  return BaseNode()

@register_ho(ho_exports)
def component(
  node: Node,
  fn_lib: FnLib,
  ho_lib: HOLib,
) -> Node | None:
  name_node = node.script
  if name_node is None: return None
  
  component_name, args_node = name_node.execute(fn_lib, ho_lib)
  if component_name.type != NodeType.TEXT:
    return None
  
  if args_node is None:
    return None
  
  args_name, script_node = args_node.execute(fn_lib, ho_lib)
  if args_name.type != NodeType.TEXT:
    return None
  
  def component_fn(
    args: list[BaseNode],
    _: Node | None = None,
    fn_lib: FnLib = {},
  ) -> BaseNode:
    if not script_node:
      return BaseNode()
    
    local_fn_scope: FnLib = {}
    for fn_keys in fn_lib:
      local_fn_scope[fn_keys] = fn_lib[fn_keys]

    saves([
      BaseNode(
        type=NodeType.TEXT,
        str_value=args_name.fetch_str()
      ),
      collection(args, None, local_fn_scope),
    ], None, local_fn_scope)
    
    result: BaseNode = script_node.execute(
      local_fn_scope,
      ho_lib,
    )[0]

    result.signal = None
    return result
  
  fn_lib[component_name.fetch_str()] = component_fn
  
  return node.next

@register_fn(fn_exports)
def saves(
  args: list[BaseNode],
  _: Node | None = None,
  fn_lib: FnLib = {},
) -> BaseNode:
  if len(args) <= 1:
    return BaseNode()

  name: str = args[0].fetch_str()
  value: BaseNode = args[1]

  def variable_fn(
    fn_args: list[BaseNode],
    node: Node | None = None,
    fn_lib: FnLib = {},
  ) -> BaseNode:
    if value.type != NodeType.GHOST:
      return value
    
    ghost_value = value.ghost_value
    if f"{ghost_value}:primary" not in fn_lib:
      return value
    
    return fn_lib[f"{ghost_value}:primary"](
      fn_args,
      node,
      fn_lib
    )

  fn_lib[name] = variable_fn
  return value

@register_fn(fn_exports)
def returns(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  if len(args) == 0:
    return BaseNode()
  
  args[0].signal = NodeSignal.RETURN
  return args[0]

