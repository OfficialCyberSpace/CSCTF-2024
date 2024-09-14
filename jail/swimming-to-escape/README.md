# Swimming to Escape

|              |                                                                                    |
| ------------ | ---------------------------------------------------------------------------------- |
| **CTF**      | [Cyberspace CTF](https://2024.csc.tf/) [(CTFtime)](https://ctftime.org/event/2428) |
| **Author**   | aa.crypto                                                                          |
| **Category** | jail                                                                               |
| **Solves**   | 11                                                                                 |

# Solution

By inputting `l` we know the flag length is 140.

Then we have this segment `>~& !- !1:! :! ?<~~` which pop 2 elements from the stack for `register` number of times.

So we first put a 2-character string in quote to put them into the stack and use `+` or `-` to manipulate the number before puttting it to the register. It will reveal the flag at all even indices.

For odd indices, put an extra `~` at the end to pop one more element from the stack.
