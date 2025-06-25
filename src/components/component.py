from src.models.node_type import NodeType
from src.models.base_node import BaseNode
from src.models.node import Node, FnLib, ExecFn, HOLib, HOExecFn

from src.internals.registry import register_exec_fn, register_ho_fn

registered_exec_fns: list[ExecFn] = []
def register_fn(fn: ExecFn) -> ExecFn:
  registered_exec_fns.append(fn)
  return fn

registered_ho_fns: list[HOExecFn] = []
def register_ho(fn: HOExecFn) -> HOExecFn:
  registered_ho_fns.append(fn)
  return fn

def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  for fn in registered_exec_fns:
    register_exec_fn(fn_lib)(fn)

  for fn in registered_ho_fns:
    register_ho_fn(ho_lib)(fn)

@register_fn
def script(*_) -> BaseNode:
  return BaseNode()

@register_ho
def component(
  node: Node,
  fn_lib: FnLib,
  ho_lib: HOLib,
) -> Node | None:
  name_node = node.script
  if name_node is None: return None
  
  component_name, args_node = name_node.execute(fn_lib, ho_lib)
  if component_name.type != NodeType.STRING:
    return None
  
  if args_node is None:
    return None
  
  args_name, script_node = args_node.execute(fn_lib, ho_lib)
  if args_name.type != NodeType.STRING:
    return None
  
  def component_fn(
    args: list[BaseNode],
    _: Node | None = None,
    __: FnLib = {},
  ) -> BaseNode:
    if not script_node:
      return BaseNode()
    
    def args_fn(
      args_fn_args: list[BaseNode],
      _: Node | None = None,
      __: FnLib = {},
    ) -> BaseNode:
      index: int = int(args_fn_args[0].fetch_float())
      if index < 0 or index >= len(args):
        return BaseNode()
      
      return args[index]

    fn_lib[args_name.fetch_str()] = args_fn
    
    return script_node.execute(
      fn_lib,
      ho_lib,
    )[0]
  
  fn_lib[component_name.fetch_str()] = component_fn
  
  return node.next

@register_fn
def saves(
  args: list[BaseNode],
  _: Node | None = None,
  fn_lib: FnLib = {},
) -> BaseNode:
  if len(args) <= 1:
    return BaseNode()
  
  name: str = args[0].fetch_str()
  value: BaseNode = args[1]

  def variable_fn(*_) -> BaseNode:
    return value

  fn_lib[name] = variable_fn
  return value
