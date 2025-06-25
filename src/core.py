from __future__ import annotations

from .models.node import FnLib, HOLib, Node
from .components import setup
from .internals.parser import parse

fn_lib: FnLib = {}
ho_lib: HOLib = {}

setup(fn_lib, ho_lib)

def run_source(source: str) -> None:
  source_lines: list[str] = source.split("\n")
  root_script: Node = parse(source_lines, set(ho_lib.keys()))
  root_script.execute(fn_lib, ho_lib)

