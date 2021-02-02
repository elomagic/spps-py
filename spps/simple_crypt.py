# ${project.name}
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

import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from os.path import expanduser
import os.path

ALGORITHM = "AES"
TRANSFORMATION = "AES/GCM/NoPadding"
MASTER_KEY_FILE = expanduser("~") + "/.elomagic/masterkey"


# Returns true when value is encrypted, tagged by surrounding braces "{" and "}".
def is_encrypted_value(value):
    return value is not None and value.startswith("{") and value.endswith("}")


def get_master_key():
    """ This method works so far """
    if os.path.isfile(MASTER_KEY_FILE):
        data = open(MASTER_KEY_FILE, "r").read()
        return base64.b64decode(data)
    else:
        print("!!! Creating master key currently not implemented !!!!")
    #     result = Base64.decode(base64);
    #
    #     key = new SecretKeySpec(result, ALGORITHM);
    # } else {

        key = get_random_bytes(16)

#        cipher = AES.new(key, AES.MODE_GCM)
#        ciphertext, tag = cipher.encrypt_and_digest(data)

#        file_out = open("encrypted.bin", "wb")
#        [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
#        file_out.close()

#        KeyGenerator kg = KeyGenerator.getInstance(ALGORITHM);
#        kg.init(128);
#        key = kg.generateKey();

#        result = key.getEncoded();

#        String base64 = Base64.toBase64String(result);

#        Files.write(MASTER_KEY_FILE, Collections.singleton(base64), StandardOpenOption.CREATE_NEW);
#    }
        return key


# Creates a cipher.
def create_cipher():
    key = get_master_key()

    nonce = "0123456789abcdef".encode("ascii")

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    return cipher


# Encrypt, encoded as Base64 and encapsulate with curly bracket of a string.
def encrypt_string(value):
    b = value.encode("utf8")
    data, tag = create_cipher().encrypt_and_digest(b)

    b64 = base64.b64encode(data + tag)
    return "{" + b64.decode("utf-8") + "}"


def decrypt_string(value):
    if not is_encrypted_value(value):
        print("Given method parameter is not encrypted")
        exit()

    b64 = value[1: -1]
    data = base64.b64decode(b64.encode("ascii"))

    cypher_text = data[:-16]
    tag = data[-16:]

    cypher = create_cipher()
    b = cypher.decrypt_and_verify(cypher_text, tag)

    return b.decode("utf8")

