from setuptools import setup, find_packages
from pathlib import Path

def read_config(file: str) -> str:
  return Path(file).read_text().strip()

setup(
  name='gsam',
  include_package_data=True,
  version=read_config("VERSION"),
  packages=find_packages(),
  author='AttAditya',
  description='A compiler for the GSAM language.',
  long_description=read_config("README.md"),
  long_description_content_type='text/markdown',
  url='https://github.com/AttAditya/gsam-compiler',
  python_requires='>=3.8',
  entry_points={
    'console_scripts': [
      'gsamc=src.cli:main',
      'gsam=src.cli:main',
      'gsam-compiler=src.cli:main',
      'gsam-compiler-cli=src.cli:main',
      'gsamc-cli=src.cli:main',
    ],
  }
)

