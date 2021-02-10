#!/usr/bin/env python

"""Creates an encrypted string for a secret."""

#
# Simple Password Protection Solution for Python
#
# Copyright © 2021-present Carsten Rambow (spps.dev@elomagic.de)
#
# This file is part of Simple Password Protection Solution with Python.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import importlib.resources as pkg_resources
from . import resources
from simple_crypt import encrypt_string as encrypt

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"


def print_help():
    text = pkg_resources.read_text(resources, 'encrypt_secret.txt')
    print(text)


if "-?" in sys.argv or "-Help" in sys.argv:
    print_help()
elif "-Secret" in sys.argv:
    v = sys.argv[sys.argv.index("-Secret") + 1]
    print(encrypt(v))
else:
    print_help()
