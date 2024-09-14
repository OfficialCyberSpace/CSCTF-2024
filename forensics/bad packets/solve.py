#!/usr/bin/env python3
import base64
from Crypto import Random
from Crypto.Cipher import AES
import hashlib

class AESCipher(object):
    """
    A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
    Also ensure the coherence and the type of the data with a unicode to byte converter.
    """
    def __init__(self, key):
        self.bs = 16
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

CIPHER = ("Tr3v0rC2R0x@nd1s@w350m3#TrevorForget")
cipher = AESCipher(key=CIPHER)

# tcp.stream eq 0
# line 6569 
print(cipher.decrypt("fqroaFzMgJpFK1u6YeWMTY37yXPg/HN7hZ3QbLlCCfkMx7PF0FUJuPLbQd/lqW5Oa/Goh6h03ofrKnSM64nOnqurnS1tBZiSbyOEOsyTfwYnVHbEFsztaLw7GEauKaAVr5QkK9mcm1lBwzHpwytNig=="))