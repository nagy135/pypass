#!/bin/python
from Crypto.Cipher import AES
import base64

def encrypt(key, message):
    msg_text = message.rjust(32)
    cipher = AES.new( key.rjust(32).encode() ,AES.MODE_ECB )
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded.strip()

def decrypt(key, message):
    cipher = AES.new( key.rjust(32).encode() ,AES.MODE_ECB )
    decoded = cipher.decrypt(base64.b64decode(message))
    return decoded.strip()
