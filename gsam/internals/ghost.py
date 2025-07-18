from typing import Generator, Callable

build: Callable[
  [Callable[[], Generator[str, None, None]]],
  Generator[str, None, None]
] = lambda fn: fn()

@build
def ghost_id_generator() -> Generator[str, None, None]:
  ghost_id: int = 0

  while True:
    yield f"ghost:{ghost_id}"
    ghost_id += 1

def generate_ghost_id() -> str:
  return next(ghost_id_generator)

