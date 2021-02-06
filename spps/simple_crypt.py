#!/usr/bin/env python

"""Main package for en- and decrypt strings"""

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

import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from os.path import expanduser
import os.path
from pathlib import Path

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"

MASTER_KEY_FOLDER = expanduser("~") + "/.spps/"
MASTER_KEY_FILE = MASTER_KEY_FOLDER + "masterkey"


def is_encrypted_value(value):
    """Returns true when value is encrypted, tagged by surrounding braces "{" and "}"."""
    return value is not None and value.startswith("{") and value.endswith("}")


def create_random_key():
    """ Creates and secure random key and returns it as Base64 encoded string."""
    key = get_random_bytes(32)
    return base64.b64encode(key).decode("ascii")


def get_master_key():
    """Reads or creates the master key."""
    if os.path.isfile(MASTER_KEY_FILE):
        data = open(MASTER_KEY_FILE, "r").read()
        return base64.b64decode(data)
    else:
        key = create_random_key()

        Path(MASTER_KEY_FOLDER).mkdir(parents=True, exist_ok=True)

        file = open(MASTER_KEY_FILE, "w")
        file.write(key)
        file.close()

        return base64.b64decode(key)


def create_cipher(iv):
    """Creates a cipher."""
    key = get_master_key()

    return AES.new(key, AES.MODE_GCM, nonce=iv)


def encrypt_string(value):
    """Encrypt, encoded as Base64 and encapsulate with curly bracket of a string."""
    if value is None:
        return None

    iv = get_random_bytes(16)
    b = value.encode("utf8")
    data, tag = create_cipher(iv).encrypt_and_digest(b)

    b64 = base64.b64encode(iv + data + tag)
    return "{" + b64.decode("utf-8") + "}"


def decrypt_string(value):
    """Decrypt an encapsulate with curly bracket Base64 string."""
    if value is None:
        return None

    if not is_encrypted_value(value):
        print("Given method parameter is not encrypted")
        exit()

    b64 = value[1: -1]
    data = base64.b64decode(b64.encode("ascii"))

    iv = data[:16]
    cypher_text = data[16:-16]
    tag = data[-16:]

    cypher = create_cipher(iv)
    b = cypher.decrypt_and_verify(cypher_text, tag)

    return b.decode("utf8")

