from src.models.node import Node, FnLib, ExecFn, HOLib, HOExecFn

from src.internals.registry import (
  register_ho,
  setup as setup_registry
)

fn_exports: list[ExecFn] = []
ho_exports: list[HOExecFn] = []
def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_registry(fn_lib, ho_lib, fn_exports, ho_exports)

@register_ho(ho_exports)
def loop(
  node: Node,
  fn_lib: FnLib,
  ho_lib: HOLib,
) -> Node | None:
  condition_node = node.script
  if condition_node is None: return node.next

  condition, loop_node = condition_node.execute(fn_lib, ho_lib)
  
  while condition.fetch_bool() and loop_node:
    loop_node.execute(fn_lib, ho_lib)
    condition, loop_node = condition_node.execute(fn_lib, ho_lib)
  
  return node.next

