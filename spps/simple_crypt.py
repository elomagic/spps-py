#!/usr/bin/env python

"""Main package for en- and decrypt strings by using Powershell 7 or higher"""

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

import subprocess
import codecs
import base64
from os.path import expanduser

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"

MASTER_KEY_FOLDER = expanduser("~") + "/.spps/"
MASTER_KEY_FILE = MASTER_KEY_FOLDER + "masterkey"


def is_encrypted_value(value):
    """Returns true when value is encrypted, tagged by surrounding braces "{" and "}"."""
    return value is not None and value.startswith("{") and value.endswith("}")


def encrypt_string(value):
    """Encrypt, encoded as Base64 and encapsulate with curly bracket of a string."""

    if value is None:
        return None

    cmd = "echo $(ConvertFrom-SecureString $(ConvertTo-SecureString \"{}\" -AsPlainText -Force))"

    process = subprocess.Popen(["pwsh", "-Command", cmd.format(value)], stdout=subprocess.PIPE)
    output = process.stdout.readline()
    process.poll()

    line = output.decode("ascii").replace("\n", "").replace("\r", "")
    b64 = codecs.encode(codecs.decode(line, 'hex'), 'base64').decode().replace('\n', '')

    return "{" + b64 + "}"


def decrypt_string(value):
    """Decrypt an encapsulate with curly bracket Base64 string."""
    if value is None:
        return None

    if not is_encrypted_value(value):
        print("Given method parameter is not encrypted")
        exit()

    b64 = value[1: -1]
    data = base64.b64decode(b64.encode("ascii")).hex()

    cmd = "echo $(ConvertFrom-SecureString $(ConvertTo-SecureString \"{}\" -Force) -AsPlainText)"

    process = subprocess.Popen(["pwsh", "-Command", cmd.format(data)], stdout=subprocess.PIPE)
    output = process.stdout.readline()
    process.poll()

    result = output.decode("utf8")

    return result

