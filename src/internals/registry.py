from typing import Callable

from src.models.node import (
  ExecFn,
  FnLib,
  HOExecFn,
  HOLib,
)

def register_exec_fn(
  lib: FnLib,
) -> Callable[[ExecFn], ExecFn]:
  def decorator(fn: ExecFn) -> ExecFn:
    lib[fn.__name__] = fn
    return fn
  
  return decorator

def register_ho_fn(
  lib: HOLib,
) -> Callable[[HOExecFn], HOExecFn]:
  def decorator(fn: HOExecFn) -> HOExecFn:
    lib[fn.__name__] = fn
    return fn
  
  return decorator

