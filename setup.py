#!/usr/bin/env python

"""Packaging script."""

from setuptools import setup, find_packages

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_text = f.read()

setup(
    name="spps",
    version="1.0.0",
    description="Simple Password Protection Solution for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carsten Rambow",
    author_email="spps.dev@elomagic.de",
    url="https://github.com/elomagic/spps-py",
    license=license_text,
    python_requires=">=3.9",
    packages=find_packages(exclude=('tests', 'docs'))
)
