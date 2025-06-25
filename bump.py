def read_config(file: str) -> str:
  with open(file, "r") as config_file:
    return config_file.read().strip()

def update_config(file: str, value: str) -> None:
  with open(file, "w") as config_file:
    config_file.write(value)

version_data = read_config("VERSION").split(".")
version_data[2] = str(int(version_data[2]) + 1)
version_data = ".".join(version_data)

update_config("VERSION", version_data)

