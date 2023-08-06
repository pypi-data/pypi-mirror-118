#!/usr/bin/env python

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
	name="openspace",
	version="0.1.1",
	description="Public package for various space operations applications",
	long_description=long_description,
	author="Brandon Sexton",
	author_email="brandon.sexton.1@outlook.com",
	packages=find_packages()
	)
