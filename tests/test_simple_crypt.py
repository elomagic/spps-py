from spps import simple_crypt


def test_encrypt_string():
    assert len(simple_crypt.encrypt_string("secret")) == 54
