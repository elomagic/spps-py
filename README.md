# spps-py

Simple Password Protection Solution for Python

---

[![Build Status](https://travis-ci.com/elomagic/spps-py.svg?branch=main)](https://travis-ci.com/elomagic/spps-py)
[![Coverage Status](https://coveralls.io/repos/github/elomagic/spps-py/badge.svg?branch=main)](https://coveralls.io/github/elomagic/spps-py?branch=main)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/pypi/v/spps-py.svg)](https://pypi.python.org/pypi/spps-py/)
[![Python versions](https://img.shields.io/pypi/pyversions/spps-py.svg)](https://pypi.python.org/pypi/spps-py/)
[![GitHub issues](https://img.shields.io/github/issues-raw/elomagic/spps-py)](https://github.com/elomagic/spps-py/issues)

The SPPS is a lightweight solution to protect / hide your password or anything else from your code.

## Features

* AES 256 CGM en-/decryption
* Cross programming languages support (Java, Python)

## Concept

This solution helps one to accidentally publish secrets unintentionally by splitting the secret into an encrypted part and a private key. 
The private key is kept separately from the rest, in a secure location for the authorized user only.

The private key is randomized for each user on each system and is therefore unique. This means that if someone has the encrypted secret, 
they can only read it if they also have the private key. You can check this by trying to decrypt the encrypted secret with another user or another system. You will not succeed.

A symmetrical encryption based on the AES-GCM 256 method is used. See also https://en.wikipedia.org/wiki/Galois/Counter_Mode

By default, the private key is stored in a file "/.sbbs/masterkey" of the user home folder.

Keep in mind that anyone who has access to the user home or relocation folder also has access to the master key !!!!

## Example

```python
from spps import simple_crypt

encryptedSecret = simple_crypt.encrypt_string("My Secret")
print("My encrypted secret is {}".format(encryptedSecret))

secret = simple_crypt.decrypt_string(encryptedSecret)
print("...and my secret is: {}".format(secret))
```

## How to create a master key

### Create a master in your home folder:

```bash  
python create_master_key.py
```

The settings file ```'~/.spps/masterkey'``` in your home folder will look like:

```properties
key=5C/Yi6+hbgRwIBhXT9PQGi83EVw2Oe6uttRSl4/kLzc=
relocation=
```

### Alternative, create a master key on a removable device:

```bash
python create_master_key.py -relocation=/Volumes/usb-stick
```

The settings file ```'~/.spps/masterkey'``` in your home folder will look like:

```properties
key=
relocation=/Volumes/usb-stick
```

...and in the relocation folder look like:

```properties
key=5C/Yi6+hbgRwIBhXT9PQGi83EVw2Oe6uttRSl4/kLzc=
relocation=
```

## How to create an encrypted password

...

``` python
```

##