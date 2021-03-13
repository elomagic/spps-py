#!/usr/bin/env python

"""Helper class for parsing command line."""

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

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"


def contains_option(option):
    """
    Check on sys.argv containing the given option.

    :param option: Argument to check
    :return: Returns true when option in list of args. Otherwise false
    """
    return option in sys.argv


def get_value_of_option(option, default_value=None):
    """
    Get value of key.

    :param option: Value of key to get
    :param default_value: Default value when key doesn't exists
    :return: Returns value of option when in list of args. Otherwise default value. By default, default value is None.
    """
    if not contains_option(option):
        return default_value

    return sys.argv[sys.argv.index(option) + 1]
