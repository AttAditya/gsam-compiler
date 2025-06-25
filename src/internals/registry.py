from typing import Callable

from src.models.node import (
  ExecFn,
  FnLib,
  HOExecFn,
  HOLib,
)

def rename_fn(name: str) -> Callable[[ExecFn], ExecFn]:
  def decorator(fn: ExecFn) -> ExecFn:
    fn.__name__ = name
    return fn
  
  return decorator

def rename_ho(name: str) -> Callable[[HOExecFn], HOExecFn]:
  def decorator(fn: HOExecFn) -> HOExecFn:
    fn.__name__ = name
    return fn
  
  return decorator

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

def register_fn(
  lib: list[ExecFn]
) -> Callable[[ExecFn], ExecFn]:
  def decorator(fn: ExecFn) -> ExecFn:
    lib.append(fn)
    return fn
  
  return decorator

def register_ho(
  lib: list[HOExecFn]
) -> Callable[[HOExecFn], HOExecFn]:
  def decorator(fn: HOExecFn) -> HOExecFn:
    lib.append(fn)
    return fn
  
  return decorator

def setup(
  fn_lib: FnLib,
  ho_lib: HOLib,
  registered_exec_fns: list[ExecFn],
  registered_ho_fns: list[HOExecFn],
) -> None:
  for fn in registered_exec_fns:
    register_exec_fn(fn_lib)(fn)

  for fn in registered_ho_fns:
    register_ho_fn(ho_lib)(fn)

