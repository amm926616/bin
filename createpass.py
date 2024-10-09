#! /usr/bin/env python

from key import get_key
from encrypt import Encryptor

key = get_key()
print("key:\n", key)
encryptor = Encryptor(key)
passcode = encryptor.encrypt()
print("passcode:\n", passcode)


