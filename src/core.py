from __future__ import annotations

from models.node import FnLib, HOLib, Node
from components import setup
from internals.parser import parse

fn_lib: FnLib = {}
ho_lib: HOLib = {}

setup(fn_lib, ho_lib)

sample = "samples/s_hello_world/sample_hello_world.gsam"
sample = "samples/s_99_bottles/sample_99_bottles.gsam"

file = open(sample, "r")
source = file.read().split("\n")
file.close()

root_script: Node = parse(source, set(ho_lib.keys()))
root_script.execute(fn_lib, ho_lib)

