from src.models.node_type import NodeType
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

@register_ho
def loop(
  node: Node,
  fn_lib: FnLib,
  ho_lib: HOLib,
) -> Node | None:
  condition_node = node.script
  if condition_node is None: return node.next

  condition, loop_node = condition_node.execute(fn_lib, ho_lib)
  if condition.type != NodeType.BOOLEAN:
    return node.next
  
  while condition.fetch_bool() and loop_node:
    loop_node.execute(fn_lib, ho_lib)
    condition, loop_node = condition_node.execute(fn_lib, ho_lib)
  
  return node.next

