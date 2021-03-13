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

import sys
import base64
from pkg_resources import resource_string
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from os.path import expanduser
import os.path
from spps import argument_parser as ap

__author__ = "Carsten Rambow"
__copyright__ = "Copyright 2021-present, Carsten Rambow (spps.dev@elomagic.de)"
__license__ = "Apache-2.0"

DEFAULT_SETTINGS_FILE = expanduser("~") + os.path.sep + ".spps" + os.path.sep + "settings"
__settings_file = DEFAULT_SETTINGS_FILE


def _read_property_(key, file=None):
    """
    Do not use this method from your project!

    :param key: Key to get value from
    :param file: File to read key value from
    :return: Returns the property value or None when key doesn't exists
    """

    if file is None:
        file = __settings_file

    if not os.path.isfile(file):
        raise FileNotFoundError("Unable to find private key. One reason is that you location doesn't exists or "
                                "have at first you to create a private key.")

    with open(file) as f:
        for line in f:
            if line.startswith(key + "="):
                return line[len(key)+1:].replace("\n", "").replace("\r", "")

    return None


def _create_file(relocation, force, file=None):
    """
    Please do not use this method from your project!

    :param relocation:
    :param force:
    :param file:
    """

    if relocation is not None:
        _create_file(None, force, relocation)

    private_key = base64.b64encode(get_random_bytes(32)).decode("ascii")

    if file is None:
        file = __settings_file

    if os.path.isfile(file) and not force:
        raise FileExistsError("Private key file \"{}\" already exists. Use parameter \"-Force\" to overwrite it."
                              . format(file))

    Path(file).parent.mkdir(parents=True, exist_ok=True)

    k = private_key if relocation is None else ""
    r = relocation if relocation is not None else ""

    file = open(file, "w")
    file.writelines([
        "key=" + k + "\n",
        "relocation=" + r + "\n"
    ])
    file.close()


def _create_cipher(iv):
    """
    Creates a cipher. Please do not use his method.

    :param iv: Initialization vector
    :return: Returns a cipher
    """

    relocation = _read_property_("relocation")
    file = __settings_file if relocation is None or relocation == "" else relocation
    value = _read_property_("key", file)

    key = base64.b64decode(value)

    return AES.new(key, AES.MODE_GCM, nonce=iv)


def is_encrypted_value(value):
    """
    Checks value on surrounding braces.

    :param value: Value to check
    :return: Returns true when value is encrypted, tagged by surrounding braces "{" and "}".
    """
    return value is not None and value.startswith("{") and value.endswith("}")


def encrypt_string(value):
    """
    Encrypt, encoded as Base64 and encapsulate with curly bracket of a string.

    :param value: Value to encrypt
    :return: Returns an Base64 string and encapsulate with curly brackets or None when given argument is also None
    """

    if value is None:
        return None

    iv = get_random_bytes(16)
    b = value.encode("utf8")
    data, tag = _create_cipher(iv).encrypt_and_digest(b)

    b64 = base64.b64encode(iv + data + tag)
    return "{" + b64.decode("utf-8") + "}"


def decrypt_string(value):
    """
    Decrypt an encapsulate with curly bracket Base64 string.

    :param value: Base64 encoded string to decrypt
    :return: Returns a decrypted string or None when given argument is also None
    """

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


def set_settings_file(file):
    """
    Set an alternative default settings file instead of default "${user.home}/.spps/settings".

    An application can use this feature to prevent sharing of the private key with other applications.

    :param file: Alternative settings file or None to use the default file.
    :return: Returns True when successful changed and False when file already set
    """
    global __settings_file
    __settings_file = DEFAULT_SETTINGS_FILE if file is None else file


def print_help():
    text = resource_string('spps.resources', 'simple_crypt.txt').decode('ascii')
    print(text)


def main():
    if ap.contains_option("-Secret"):
        print(encrypt_string(ap.get_value_of_option(sys.argv, "-Secret")))
    elif ap.contains_option("-CreatePrivateKey"):
        force = "-Force" in sys.argv
        r = ap.get_value_of_option("-Relocation")
        file = ap.get_value_of_option("-File")
        _create_file(r, force, file)
    else:
        print_help()


if __name__ == '__main__':
    main()
