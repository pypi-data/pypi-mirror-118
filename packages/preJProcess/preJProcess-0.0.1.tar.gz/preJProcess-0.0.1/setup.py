# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 17:46:44 2021

@author: jbhatt
"""

from setuptools import setup

setup(
      name = 'preJProcess',
      version='0.0.1',
      description='Pre processing the Data Frame',
      py_modules=["preProcess"],
      package_dir={'':"src"},
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
       ],
      url = "https://github.com/jeetbhatt-sys/DataPreProcess",
      author = "Jeet Bhatt",
      author_email="jeetbhatt.va@gmail.com",
      )