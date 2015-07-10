#!/usr/bin/env python
from setuptools import setup, find_packages
from pip.req import parse_requirements

NAME = "standuino"
VERSION = "0.1.0"

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    scripts=["scripts/standuino"],
)
