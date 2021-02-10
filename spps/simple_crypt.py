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
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from os.path import expanduser
import os.path

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"

SPPS_FOLDER = expanduser("~") + "/.spps/"
MASTER_KEY_FILE = SPPS_FOLDER + "masterkey"
KEY_FILENAME = "masterkey"


def _read_property_(key, location=None):
    """Do not use this method from your project!"""
    if location is None:
        location = MASTER_KEY_FILE

    if not os.path.isfile(location):
        raise FileNotFoundError("Unable to find settings file. At first you have to create a master key.")

    with open(location) as f:
        for line in f:
            if line.startswith(key + "="):
                return line[len(key)+1:].replace("\n", "").replace("\r", "")

    raise ValueError("Key {} doesn't exists.".format(key))


def _create_file(relocation, force, path=None):
    """Do not use this method from your project!"""
    if relocation is not None:
        _create_file(None, force, relocation)

    master_key = base64.b64encode(get_random_bytes(32)).decode("ascii")

    if path is None:
        path = SPPS_FOLDER

    file = path + KEY_FILENAME

    if os.path.isfile(file) and not force:
        raise FileExistsError("Master key file \"{}\" already exists. Use parameter \"-Force\" to overwrite it.". format(file))

    Path(path).mkdir(parents=True, exist_ok=True)

    # TODO Ask for master key location

    k = master_key if relocation is None else ""
    r = relocation if relocation is not None else ""

    file = open(file, "w")
    file.writelines([
        "key=" + k + "\n",
        "relocation=" + r + "\n"
    ])
    file.close()


def _create_cipher(iv):
    """Creates a cipher."""

    if not os.path.isfile(MASTER_KEY_FILE):
        raise FileNotFoundError("Unable to find master key. One reason is that you location doesn't exists or at first you have to create a master key.")

    value = _read_property_("key")

    key = base64.b64decode(value)

    return AES.new(key, AES.MODE_GCM, nonce=iv)


def is_encrypted_value(value):
    """Returns true when value is encrypted, tagged by surrounding braces "{" and "}"."""
    return value is not None and value.startswith("{") and value.endswith("}")


def encrypt_string(value):
    """Encrypt, encoded as Base64 and encapsulate with curly bracket of a string."""
    if value is None:
        return None

    iv = get_random_bytes(16)
    b = value.encode("utf8")
    data, tag = _create_cipher(iv).encrypt_and_digest(b)

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

    cypher = _create_cipher(iv)
    b = cypher.decrypt_and_verify(cypher_text, tag)

    return b.decode("utf8")

