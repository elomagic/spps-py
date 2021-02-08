#!/usr/bin/env python

from spps import simple_crypt
import codecs
import base64


def test_Anything():
    line = "01000000d08c9ddf0115d1118c7a00c04fc297eb010000008efa4f665d7a9d409ee9e96e439d21520000000002000000000003660000c000000010000000e70a8c2415e2699fefe777870a79a4ca0000000004800000a000000010000000e1fd131f50e6fa49bd774768d611237e10000000bf7097a6a4884b1867fbc185f0d9e29214000000b56966ea595997a3890fb5fe499673aa49cd1403"
    b64 = codecs.encode(codecs.decode(line, 'hex'), 'base64').decode().replace('\n', '')
    print(b64)
    #data = base64.b64decode(b64.encode("ascii")).decode("ascii")
    #print(data)
    # base64.b64decode(b64.encode("ascii"))


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
