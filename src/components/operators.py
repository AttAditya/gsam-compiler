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
def concatenate(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  result = ""
  for arg in args:
    result += arg.fetch_str()
  
  return BaseNode(
    type=NodeType.STRING,
    str_value=result
  )

@register_fn
def add(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  result: float = 0.0
  for arg in args:
    result += arg.fetch_float()
  
  return BaseNode(
    type=NodeType.NUMERIC,
    float_value=result
  )


@register_fn
def multiply(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  result: float = 1.0
  for arg in args:
    result *= arg.fetch_float()
  
  return BaseNode(
    type=NodeType.NUMERIC,
    float_value=result
  )

@register_fn
def subtract(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  args.append(BaseNode(type=NodeType.NUMERIC, float_value=0.0))
  args.append(BaseNode(type=NodeType.NUMERIC, float_value=0.0))
  
  result: float = args[0].fetch_float() - args[1].fetch_float()
  return BaseNode(
    type=NodeType.NUMERIC,
    float_value=result
  )

@register_fn
def divide(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  args.append(BaseNode(type=NodeType.NUMERIC, float_value=0.0))
  args.append(BaseNode(type=NodeType.NUMERIC, float_value=1.0))
  
  result: float = args[0].fetch_float() / args[1].fetch_float()
  return BaseNode(
    type=NodeType.NUMERIC,
    float_value=result
  )

@register_fn
def equals(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  if len(args) < 2:
    return BaseNode(type=NodeType.BOOLEAN, bool_value=False)
  
  types = set(arg.type for arg in args)
  if len(types) > 1:
    return BaseNode(type=NodeType.BOOLEAN, bool_value=False)
  
  if NodeType.NUMERIC in types:
    result: bool = args[0].fetch_float() == args[1].fetch_float()
  elif NodeType.BOOLEAN in types:
    result: bool = args[0].fetch_bool() == args[1].fetch_bool()
  else:
    result: bool = args[0].fetch_str() == args[1].fetch_str()

  return BaseNode(
    type=NodeType.BOOLEAN,
    bool_value=result
  )

@register_fn
def not_equals(
  args: list[BaseNode],
  _: Node | None = None,
  __: FnLib = {},
) -> BaseNode:
  return BaseNode(
    type=NodeType.BOOLEAN,
    bool_value=not equals(args, None, __).fetch_bool()
  )

