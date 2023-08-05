#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
  name='pyexporter',
  version='0.0.1',
  license="MIT",
  author="Sergey Lunkov",
  package_dir={'pyexporter': 'src'},
  packages=['pyexporter'],
  install_requires=[
    "python-dotenv",
    "psycopg2",
    "pylightxl",
    "sysrsync",
  ],
)
