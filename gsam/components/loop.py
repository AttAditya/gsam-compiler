from gsam.models.node_signal import NodeSignal
from gsam.models.node import Node, FnLib, ExecFn, HOLib, HOExecFn

from gsam.internals.registry import (
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
  if not condition.fetch_bool(): return node.next
  if loop_node is None: return node.next

  result, _ = loop_node.execute(fn_lib, ho_lib)
  if result.signal == NodeSignal.RETURN:
    return Node(
      executes="base",
      value=result,
    )

  return node

