from src.models.node_type import NodeType
from src.models.node import ExecFn, HOExecFn, FnLib, HOLib
from src.models.base_node import BaseNode

from src.internals.registry import (
  register_fn,
  rename_fn,
  setup as setup_registry
)

fn_exports: list[ExecFn] = []
ho_exports: list[HOExecFn] = []
def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_registry(fn_lib, ho_lib, fn_exports, ho_exports)

@register_fn(fn_exports)
def output(
  args: list[BaseNode],
  *_,
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

@register_fn(fn_exports)
@rename_fn("input")
def input_fn(
  args: list[BaseNode],
  *_,
) -> BaseNode:
  if not args:
    return BaseNode()
  
  prompt: str = ""
  if len(args) >= 1:
    prompt = args[0].fetch_str()

  input_value = input(prompt)

  return BaseNode(
    type=NodeType.TEXT,
    str_value=input_value
  )

