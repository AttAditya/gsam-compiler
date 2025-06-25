from src.models.node import FnLib, HOLib

from .clio import setup as setup_clio
from .literals import setup as setup_literals
from .component import setup as setup_component
from .operators import setup as setup_operators
from .loops import setup as setup_loops

def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_clio(fn_lib, ho_lib)
  setup_literals(fn_lib, ho_lib)
  setup_component(fn_lib, ho_lib)
  setup_operators(fn_lib, ho_lib)
  setup_loops(fn_lib, ho_lib)

