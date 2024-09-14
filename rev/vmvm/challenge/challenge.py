from vm_gen import VMBytecodeGenerator, Regs
import random

vm = VMBytecodeGenerator()
vm.set_entry_point("main")

# counts number of set bits in a number
# R1: number to count set bits
vm.label("count_bits")
vm.push(Regs.R1)
vm.push(Regs.R2)
vm.mov_rr(Regs.R2, Regs.R1)
vm.div_rc(Regs.R2, 2 ** 1)
vm.and_rc(Regs.R2, 0x55555555)
vm.sub_rr(Regs.R1, Regs.R2)
vm.mov_rr(Regs.R2, Regs.R1)
vm.and_rc(Regs.R2, 0x33333333)
vm.div_rc(Regs.R1, 2 ** 2)
vm.and_rc(Regs.R1, 0x33333333)
vm.add_rr(Regs.R1, Regs.R2)
vm.mov_rr(Regs.R2, Regs.R1)
vm.div_rc(Regs.R2, 2 ** 4)  
vm.add_rr(Regs.R1, Regs.R2)
vm.and_rc(Regs.R1, 0x0F0F0F0F)
vm.mul_rc(Regs.R1, 0x01010101)
vm.div_rc(Regs.R1, 2 ** 24)
vm.mov_rr(Regs.R0, Regs.R1)
vm.pop(Regs.R2)
vm.pop(Regs.R1)
vm.ret()

# opcodes for mini inner vm
OP_TRUE = 15
OP_FALSE = 16
OP_FAIL = 17
OP_SUCCESS = 18

# run instructions from the inner "vm" (i gave up on making the inner vm good so it's this now)
# R1: address of instruction (i am aware the 2nd part of the instruction isnt used but idc)
vm.label("run_insn")
vm.push(Regs.R1)
vm.push(Regs.R2)
vm.push(Regs.R3)
vm.load_rr(Regs.R2, Regs.R1)
vm.add_rc(Regs.R1, 4)
vm.load_rr(Regs.R3, Regs.R1)
vm.mov_rr(Regs.R1, Regs.R2)
vm.call("count_bits")
vm.cmp_rc(Regs.R0, OP_FAIL)
vm.jz("do_op_fail")
vm.cmp_rc(Regs.R0, OP_SUCCESS)
vm.jz("do_op_success")
vm.cmp_rc(Regs.R0, OP_FALSE)
vm.jz("do_op_false")
vm.cmp_rc(Regs.R0, OP_TRUE)
vm.jz("do_op_true")

question_str = vm.make_string("???\n")
vm.print_str(question_str)
vm.halt()

vm.label("do_op_false")
vm.mov_rc(Regs.R0, 0)
vm.jmp("cleanup")

vm.label("do_op_true")
vm.mov_rc(Regs.R0, 1)
vm.jmp("cleanup")

vm.label("do_op_fail")
fail_str = vm.make_string("Nuh uh\n")
vm.print_str(fail_str)
vm.halt()

vm.label("do_op_success")
success_str = vm.make_string("Yay\n")
vm.print_str(success_str)
vm.halt()

vm.label("cleanup")
vm.pop(Regs.R3)
vm.pop(Regs.R2)
vm.pop(Regs.R1)
vm.ret()

# too lazy to comment the rest of this, gl

def gen_insn_opcode(op):
    set_bits = random.sample(range(32), k=op)
    return sum(1 << x for x in set_bits)

def gen_level(char):
    GOAL = ord(char) ^ 69
    generator = (
        gen_insn_opcode(OP_TRUE if x == GOAL else OP_FALSE).to_bytes(4, 'little') + random.randint(0, 2**32-1).to_bytes(4, 'little')
        for x in range(256)
    )
    
    return b"".join(generator)

FLAG = "CSCTF{i_would_make_gross_hidden_crypto_but_idk_crypto_f5f04dd12}"
assert len(FLAG) == 64

vm.label("main")
prompt = vm.make_string("Flag > ")
vm.print_str(prompt)

valid_buf = vm.make_buffer(8)
levels = vm.make_bytestring(b"".join(gen_level(char) for char in FLAG))

p32 = lambda b: int.from_bytes(b, 'little')
vm.mov_rc(Regs.R6, p32(b"hint"))
vm.xor_rc(Regs.R6, p32(b"this"))
vm.mul_rc(Regs.R6, p32(b"solv"))
vm.add_rc(Regs.R6, p32(b"100%"))
vm.and_rc(Regs.R6, p32(b"uses"))
vm.sub_rc(Regs.R6, p32(b"LLL!"))
vm.xor_rc(Regs.R6, 0x10d406b9)

vm.mov_rc(Regs.R5, 0)
vm.label("loop_start")
vm.cmp_rr(Regs.R5, Regs.R6)
vm.jz("check_valid")

vm.mov_rr(Regs.R4, Regs.R5)
vm.mul_rc(Regs.R4, 256 * 8)
vm.add_rc(Regs.R4, levels)
vm.read_byte(Regs.R1)
vm.xor_rc(Regs.R1, 69)
vm.mul_rc(Regs.R1, 8)
vm.add_rr(Regs.R1, Regs.R4)
vm.call("run_insn")
vm.mov_rr(Regs.R4, Regs.R5)
vm.div_rc(Regs.R4, 32)
vm.mul_rc(Regs.R4, 4)
vm.mov_rc(Regs.R3, valid_buf)
vm.add_rr(Regs.R4, Regs.R3)
vm.load_rr(Regs.R3, Regs.R4)
vm.mul_rc(Regs.R3, 2 ** 1)
vm.add_rr(Regs.R3, Regs.R0)
vm.store_rr(Regs.R4, Regs.R3)
vm.add_rc(Regs.R5, 1)
vm.jmp("loop_start")

vm.label("check_valid")

num = 0x20000
while (num & 0x20000) != 0:
    # using some random bit to determine if player got the flag or not
    num = gen_insn_opcode(OP_FAIL)

vm.mov_rc(Regs.R1, valid_buf)
vm.load_rr(Regs.R2, Regs.R1)
vm.add_rc(Regs.R1, 4)
vm.load_rr(Regs.R1, Regs.R1)
vm.mov_rc(Regs.R3, num)
vm.sub_rr(Regs.R1, Regs.R2)
vm.jnz("do_final_insn")
vm.add_rc(Regs.R2, 1)
vm.jnz("do_final_insn")
vm.add_rc(Regs.R3, 0x20000)

vm.label("do_final_insn")
vm.mov_rc(Regs.R1, valid_buf)
vm.store_rr(Regs.R1, Regs.R3)
vm.call("run_insn")
vm.halt()

vm.save("vmvm.vm")