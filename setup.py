#!/usr/bin/env python

"""Packaging script."""

from setuptools import setup, find_packages

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"

with open('README.md') as f:
    readme = f.read()

setup(
    name="spps",
    version="1.0.0rc1",
    description="Simple Password Protection Solution for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carsten Rambow",
    author_email="spps.dev@elomagic.de",
    url="https://github.com/elomagic/spps-py",
    project_urls={
        'Source': 'https://github.com/elomagic/spps-py',
        'Tracker': 'https://github.com/elomagic/spps-py/issues'
    },
    license="Apache-2.0",
    python_requires=">=3.9",
    keywords=["encrypt", "decrypt", "password", "security", "hide", "protect", "key", "secret", "AES", "GCM"],
    packages=find_packages(exclude=('tests', 'docs'))
)
