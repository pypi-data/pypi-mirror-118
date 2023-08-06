# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 17:46:44 2021

@author: jbhatt
"""

from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
      name = 'preJPProcess',
      version='0.0.1',
      description='Pre processing the Data Frame',
      py_modules=["preJPProcess"],
      package_dir={'':"src"},
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
       ],
      url = "https://github.com/jeetbhatt-sys/DataPreProcess",
      author = "Jeet Bhatt",
      author_email="jeetbhatt.va@gmail.com",
      long_description=long_description,
      long_description_content_type='text/markdown',
      )