#!/usr/bin/env python

from spps import simple_crypt

encryptedSecret = simple_crypt.encrypt_string("My Secret")
print("My encrypted secret is {}".format(encryptedSecret))

secret = simple_crypt.decrypt_string(encryptedSecret)
print("...and my secret is: {}".format(secret))


