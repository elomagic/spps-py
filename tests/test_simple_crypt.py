#!/usr/bin/env python

from spps import simple_crypt


def test_is_encrypted_value():
    assert simple_crypt.is_encrypted_value("{abc}")
    assert not simple_crypt.is_encrypted_value("abc}")
    assert not simple_crypt.is_encrypted_value("{abc")
    assert not simple_crypt.is_encrypted_value("abc")


def test_encrypt_string():
    assert len(simple_crypt.encrypt_string("secret")) == 54


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
