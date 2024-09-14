# Byte Modification Service

|              |                                                                                    |
| ------------ | ---------------------------------------------------------------------------------- |
| **CTF**      | [Cyberspace CTF](https://2024.csc.tf/) [(CTFtime)](https://ctftime.org/event/2428) |
| **Author**   | aa.crypto                                                                          |
| **Category** | pwn                                                                                |
| **Solves**   | 70                                                                                 |

# Solution

1. Notice the program is writable
2. Notice `win` and `bye` function are close to each other
3. Notice the format string vuln

## Solution

1. Use the stack pointer which reference to an address in the `main` function (the return address to `main` from `vuln`)
2. Choose index 0 and xor the address to the required byte of the call instruction to modify it to call `win` instead of `bye`
3. Format string vuln to write that single byte
