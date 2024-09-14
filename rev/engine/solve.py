#!/usr/bin/env python3

from Crypto.Cipher import Salsa20
import binascii
from pwn import xor

def main():
    keyseed = [186, 223, 66, 163, 183, 202, 114, 209, 151, 216, 114, 90, 119, 159, 12, 51, 235, 143, 19, 159, 26, 210, 152, 59, 113, 204, 234, 245, 55, 214, 38, 52]
    keyseed = bytes(keyseed)
    nonceseed = [66, 235, 154, 153, 215, 45, 46, 60]
    nonceseed = bytes(nonceseed)

    ciphertext = binascii.unhexlify("456c09423ba01203c6333b6bbcdc6dfd009128cc266ff9fd831ea638e404c48d315ee57caf5f226f2d")
    cipher = Salsa20.new(key=keyseed, nonce=nonceseed)
    plaintext = cipher.decrypt(ciphertext)
    print("Flag: ", plaintext)

if __name__ == '__main__':
    main()