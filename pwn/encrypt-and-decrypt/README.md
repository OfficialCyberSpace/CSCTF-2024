# Encrypt and Decrypt

|              |                                                                                    |
| ------------ | ---------------------------------------------------------------------------------- |
| **CTF**      | [Cyberspace CTF](https://2024.csc.tf/) [(CTFtime)](https://ctftime.org/event/2428) |
| **Author**   | aa.crypto                                                                          |
| **Category** | pwn, crypto                                                                        |
| **Solves**   | 15                                                                                 |

# Solution

This is a pwn + crypto challenge.

1. For pwn, it's a 64-bit binary which encrypt and decrypt payloads with format string vuln and buffer overflow for the decrypted text.
2. For crypto, it's an encryption of AES CBC mode, but the encryption only handles <=16 bytes of payload with capital letter only, the decryption, on the other hand, works with arbitrary length, which triggers the buffer overflow.

First we leak canary, piebase and libc base via `%47$lx`, `%49$lx` and `%51$lx`, by using AES CBC property.

Then craft the payload using ROP chain of the found libc version. and craft the required payload including the canary.

Finally craft the encrypted payload via CBC xor by controlling each block of ciphertext backwards.
