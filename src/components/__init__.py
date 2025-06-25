from src.models.node import FnLib, HOLib

from .console import setup as setup_clio
from .literal import setup as setup_literals
from .component import setup as setup_component
from .operator import setup as setup_operators
from .loop import setup as setup_loops
from .control import setup as setup_control
from .collection import setup as setup_collection

def setup(fn_lib: FnLib, ho_lib: HOLib) -> None:
  setup_clio(fn_lib, ho_lib)
  setup_literals(fn_lib, ho_lib)
  setup_component(fn_lib, ho_lib)
  setup_operators(fn_lib, ho_lib)
  setup_loops(fn_lib, ho_lib)
  setup_control(fn_lib, ho_lib)
  setup_collection(fn_lib, ho_lib)

