#!/usr/bin/env python

import sys
import tempfile
import shutil
import pytest
from io import StringIO
from os.path import expanduser
from os import path

from spps import simple_crypt

backup = None
SETTINGS = expanduser("~") + "/.spps/settings"


def setup_module(module):
    global backup

    if path.exists(SETTINGS):
        print("Backup existing settings")
        with open (SETTINGS, "r") as my_file:
            backup = my_file.read()


def teardown_module(module):
    global backup

    if backup is None:
        return

    print("Restore existing settings")
    with open (SETTINGS, "w") as my_file:
        my_file.write(backup)


def test__create_file():
    simple_crypt._create_file(None, True)
    assert len(simple_crypt._read_property_("key")) > 30
    assert len(simple_crypt._read_property_("relocation")) == 0


def test_is_encrypted_value():
    assert simple_crypt.is_encrypted_value("{abc}")
    assert not simple_crypt.is_encrypted_value("abc}")
    assert not simple_crypt.is_encrypted_value("{abc")
    assert not simple_crypt.is_encrypted_value("abc")
    assert not simple_crypt.is_encrypted_value(None)


def test_crypt_string():
    v1 = simple_crypt.encrypt_string("secret")
    v2 = simple_crypt.encrypt_string("secret")
    assert v1 != v2

    value = "secretäöüß"

    encrypted = simple_crypt.encrypt_string(value)
    assert value != encrypted
    decrypted = simple_crypt.decrypt_string(encrypted)
    assert value == decrypted

    assert simple_crypt.encrypt_string(None) is None
    assert simple_crypt.decrypt_string(None) is None


def test_set_settings_file():

    temp_folder = tempfile.mkdtemp()
    settings_file = temp_folder + "/alternativeSettings"
    assert not path.exists(settings_file)

    value = "secretäöüß"
    simple_crypt._create_file(None, True)
    encrypted1 = simple_crypt.encrypt_string(value)
    assert simple_crypt.is_encrypted_value(encrypted1);
    assert value == simple_crypt.decrypt_string(encrypted1)

    simple_crypt.set_settings_file(settings_file)
    with pytest.raises(Exception):
        simple_crypt.decrypt_string(encrypted1)

    simple_crypt._create_file(None, True)
    assert path.exists(settings_file)

    encrypted2 = simple_crypt.encrypt_string(value)
    simple_crypt.set_settings_file(None)
    with pytest.raises(Exception):
        simple_crypt.decrypt_string(encrypted2)

    shutil.rmtree(temp_folder)


def test_command_line_encrypt():
    sys.argv = [
        "-Secret",
        "abc"
    ]

    old_stdout = sys.stdout
    sys.stdout = my_stdout = StringIO()

    simple_crypt.main()

    text = my_stdout.getvalue()
    sys.stdout = old_stdout

    assert simple_crypt.is_encrypted_value(text.strip())


def test_command_line_help():
    sys.argv = [ "-?" ]

    old_stdout = sys.stdout
    sys.stdout = my_stdout = StringIO()

    simple_crypt.main()

    text = my_stdout.getvalue()
    sys.stdout = old_stdout

    assert "Set an alternative setting file" in text
