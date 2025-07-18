from gsam.models.node import HOExecFn, ExecFn, FnLib, HOLib, Node

from gsam.internals.registry import (
  register_ho,
  rename_ho,
  setup as setup_registry
)

fn_exports: list[ExecFn] = []
ho_exports: list[HOExecFn] = []
def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_registry(fn_lib, ho_lib, fn_exports, ho_exports)

@register_ho(ho_exports)
@rename_ho("if")
def if_fn(
  node: Node,
  fn_lib: FnLib,
  ho_lib: HOLib,
) -> Node | None:
  condition_node = node.script
  if condition_node is None: return node.next

  condition, true_node = condition_node.execute(fn_lib, ho_lib)
  if true_node is None: return node.next
  false_node: Node | None = true_node.next

  true_node = true_node.clone()
  true_node.next = None
  
  if false_node is not None:
    false_node = false_node.clone()
  
  if condition.fetch_bool():
    return true_node
  
  return false_node

