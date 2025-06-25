from typing import Self
from sys import argv

from src.core import run_source

class CLIOption:
  option: str
  meta: str | None = None

  def __init__(
    self: Self,
    option: str = "",
    meta: str | None = None,
  ) -> None:
    self.option = option
    self.meta = meta
  
def run_file(file: str) -> None:
  source: str = ""

  try:
    with open(file, "r") as source_file:
      source = source_file.read()
      source_file.close()
  except FileNotFoundError:
    print(f"Error: File '{file}' not found.")
  
  run_source(source)

def run_options(options: list[CLIOption]) -> None:
  run_file(options[0].option)

def main() -> None:
  cli_options: list[CLIOption] = []
  meta: str | None = None

  for arg in argv[1:]:
    if arg.startswith("-"):
      meta = arg[1:]
      continue

    cli_options.append(CLIOption(
      option=arg,
      meta=meta
    ))
    meta = None
  else:
    if meta is not None:
      cli_options.append(CLIOption(
        option="",
        meta=meta
      ))

  run_options(cli_options)

