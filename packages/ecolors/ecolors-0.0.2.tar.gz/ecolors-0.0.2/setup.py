from setuptools import setup, find_packages
import codecs
from pathlib import Path

VERSION = '0.0.2'
DESCRIPTION = 'Colors for the printing functions'

def read_file(rel_path: str):
    return Path(__file__).parent.joinpath(rel_path).read_text()

# Setting up
setup(
    name="ecolors",
    version=VERSION,
    author="Electro Development",
    author_email="contactus.electro@gmail.com",
    description=DESCRIPTION,
    keywords=['python', 'colors'],
    long_description=read_file("README.md"),
)