from typing import Generator

def ghost_id_generator() -> Generator[str, None, None]:
  ghost_id = 0

  while True:
    yield f"ghost:{ghost_id}"
    ghost_id += 1

def generate_ghost_id() -> str:
  return next(ghost_id_generator())

