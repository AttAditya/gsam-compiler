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
def output(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  if not args:
    return BaseNode()
  
  converted_args: list[str] = [
    arg.fetch_str()
    for arg in args
  ]

  print(
    *converted_args,
    sep="",
    end=""
  )

  return BaseNode()

