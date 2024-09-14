from enum import Enum, auto
from abc import ABC, abstractmethod

# single file atrocity

class Regs(Enum):
    R0 = 0
    R1 = auto()
    R2 = auto()
    R3 = auto()
    R4 = auto()
    R5 = auto()
    R6 = auto()
    R7 = auto()

class Instructions(Enum):
    VM_MOV_RR = 0
    VM_MOV_RC = auto()
    VM_ADD_RR = auto()
    VM_ADD_RC = auto()
    VM_SUB_RR = auto()
    VM_SUB_RC = auto()
    VM_MUL_RR = auto()
    VM_MUL_RC = auto()
    VM_DIV_RR = auto()
    VM_DIV_RC = auto()
    VM_XOR_RR = auto()
    VM_XOR_RC = auto()
    VM_AND_RR = auto()
    VM_AND_RC = auto()
    VM_JMP_R = auto()
    VM_JMP_C = auto()
    VM_JZ = auto()
    VM_JNZ = auto()
    VM_CALL = auto()
    VM_RET = auto()
    VM_PUSH = auto()
    VM_POP = auto()
    VM_CMP_RR = auto()
    VM_CMP_RC = auto()
    VM_STORE_RR = auto()
    VM_STORE_RC = auto()
    VM_LOAD_RR = auto()
    VM_LOAD_RC = auto()
    VM_READ_BYTE = auto()
    VM_PRINT_STR = auto()
    VM_HALT = auto()
    
class Address(ABC):
    def __init__(self, addr):
        self.addr = addr

    @abstractmethod
    def get(self, vm_instance):
        pass
    
    @abstractmethod
    def get_fixed_address(self, vm_instance):
        pass

class StringAddress(Address):
    def get(self, vm_instance):
        vm_instance.unresolved_strings.append((len(vm_instance.bytecode), self))
        return 0
        
    def get_fixed_address(self, vm_instance):
        return self.addr + len(vm_instance.bytecode)
    
class BufferAddress(Address):
    def get(self, vm_instance):
        vm_instance.unresolved_buffers.append((len(vm_instance.bytecode), self))
        return 0
        
    def get_fixed_address(self, vm_instance):
        return self.addr + len(vm_instance.bytecode) + len(vm_instance.string_buffer)

class VMBytecodeGenerator:
    def __init__(self):
        self.bytecode = bytearray()
        self.string_buffer = bytearray()
        self.buffer = bytearray()
        
        self.labels: dict[str, int] = {}

        self.unresolved_jumps: list[tuple[int, str]] = []
        self.unresolved_strings: list[tuple[int, Address]] = []
        self.unresolved_buffers: list[tuple[int, Address]] = []

    def _append_uint8(self, value: int | Regs | Instructions):
        if isinstance(value, (Regs, Instructions)):
            self.bytecode.extend(value.value.to_bytes(1, 'little'))
        else:
            self.bytecode.extend(value.to_bytes(1, 'little'))

    def _append_uint32(self, value: int | Address):
        if isinstance(value, int):
            self.bytecode.extend(value.to_bytes(4, 'little'))
        else:
            self.bytecode.extend(value.get(self).to_bytes(4, 'little'))
            
    def _append_placeholder(self):
        self.bytecode.extend(b"\0\0\0\0")
            
    def _assert_instance_reg(self, reg: Regs):
        assert isinstance(reg, Regs), f"reg must be of type 'Regs' but instead got type {type(reg)!r}"

    def set_entry_point(self, entry_point: int | str):
        self.entry_point = entry_point
        self._to_set_entry = isinstance(entry_point, str)
        
    def _rr_insn(self, op, reg1, reg2):
        self._assert_instance_reg(reg1)
        self._assert_instance_reg(reg2)
        self._append_uint8(op)
        self._append_uint8(reg1)
        self._append_uint8(reg2)
    
    def _rc_insn(self, op, reg, constant):
        self._assert_instance_reg(reg)
        self._append_uint8(op)
        self._append_uint8(reg)
        self._append_uint32(constant)

    def label(self, name: str):
        self.labels[name] = len(self.bytecode)

    def mov_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_MOV_RR, reg1, reg2)

    def mov_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_MOV_RC, reg, constant)

    def add_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_ADD_RR, reg1, reg2)

    def add_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_ADD_RC, reg, constant)

    def sub_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_SUB_RR, reg1, reg2)

    def sub_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_SUB_RC, reg, constant)

    def mul_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_MUL_RR, reg1, reg2)

    def mul_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_MUL_RC, reg, constant)

    def div_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_DIV_RR, reg1, reg2)

    def div_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_DIV_RC, reg, constant)

    def xor_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_XOR_RR, reg1, reg2)

    def xor_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_XOR_RC, reg, constant)
        
    def and_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_AND_RR, reg1, reg2)

    def and_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_AND_RC, reg, constant)

    def jmp(self, label_or_reg: str | Regs):
        if isinstance(label_or_reg, str):
            self._append_uint8(Instructions.VM_JMP_C)
            self.unresolved_jumps.append((len(self.bytecode), label_or_reg))
            self._append_placeholder()
        else:
            self._assert_instance_reg(label_or_reg)
            self._append_uint8(Instructions.VM_JMP_R)
            self._append_uint8(label_or_reg)
            

    def jz(self, label: str):
        self._append_uint8(Instructions.VM_JZ)
        self.unresolved_jumps.append((len(self.bytecode), label))
        self._append_placeholder()

    def jnz(self, label: str):
        self._append_uint8(Instructions.VM_JNZ)
        self.unresolved_jumps.append((len(self.bytecode), label))
        self._append_placeholder()

    def call(self, label: str):
        self._append_uint8(Instructions.VM_CALL)
        self.unresolved_jumps.append((len(self.bytecode), label))
        self._append_placeholder()

    def ret(self):
        self._append_uint8(Instructions.VM_RET)

    def push(self, reg: Regs):
        self._assert_instance_reg(reg)
        self._append_uint8(Instructions.VM_PUSH)
        self._append_uint8(reg)

    def pop(self, reg: Regs):
        self._assert_instance_reg(reg)
        self._append_uint8(Instructions.VM_POP)
        self._append_uint8(reg)

    def cmp_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_CMP_RR, reg1, reg2)

    def cmp_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_CMP_RC, reg, constant)

    def store_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_STORE_RR, reg1, reg2)
        
    def store_rc(self, reg: Regs, constant: int | Address):
        self._rc_insn(Instructions.VM_STORE_RC, reg, constant)
        
    def load_rr(self, reg1: Regs, reg2: Regs):
        self._rr_insn(Instructions.VM_LOAD_RR, reg1, reg2)

    def load_rc(self, reg: Regs, addr: int | Address):
        self._assert_instance_reg(reg)
        self._append_uint8(Instructions.VM_LOAD_RC)
        self._append_uint8(reg)
        self._append_uint32(addr)

    def read_byte(self, reg: Regs):
        self._assert_instance_reg(reg)
        self._append_uint8(Instructions.VM_READ_BYTE)
        self._append_uint8(reg)

    def print_str(self, addr: int | Address):
        self._append_uint8(Instructions.VM_PRINT_STR)
        self._append_uint32(addr)

    def halt(self):
        self._append_uint8(Instructions.VM_HALT)
        
    def make_buffer(self, size: int):
        addr = len(self.buffer)
        self.buffer.extend(bytearray(size))
        return BufferAddress(addr)
    
    def make_bytestring(self, bytestring: bytes | bytearray):
        addr = len(self.buffer)
        self.buffer.extend(bytestring)
        return BufferAddress(addr)
    
    def make_string(self, string: str):
        addr = len(self.string_buffer)
        self.string_buffer.extend(string.encode('utf-8') + b'\0')
        return StringAddress(addr)
    
    def _resolve_entry(self):
        if getattr(self, "entry_point", None) is None:
            raise RuntimeError("Entry point not set! Use 'set_entry_point' with an address or label.")

        if not self._to_set_entry:
            return
        
        if self.entry_point not in self.labels:
            raise RuntimeError(f"label {self.entry_point!r} for entry not defined!")

        self.entry_point = self.labels[self.entry_point]

    def _resolve_jumps(self):
        for position, label in self.unresolved_jumps:
            if label not in self.labels:
                raise RuntimeError(f"Undefined label: {label}")

            jump_address = self.labels[label]
            self.bytecode[position:position+4] = jump_address.to_bytes(4, 'little')
            
    def _resolve_strings(self):
        for position, addr in self.unresolved_strings:
            self.bytecode[position:position+4] = addr.get_fixed_address(self).to_bytes(4, 'little')
            
    def _resolve_buffers(self):
        for position, addr in self.unresolved_buffers:
            self.bytecode[position:position+4] = addr.get_fixed_address(self).to_bytes(4, 'little')
            
    def _resolve_addrs(self):
        self._resolve_entry()
        self._resolve_jumps()
        self._resolve_strings()
        self._resolve_buffers()

    def generate(self):
        self._resolve_addrs()
        
        prog = b""

        # header info
        prog += (len(self.bytecode) + len(self.string_buffer) + len(self.buffer)).to_bytes(4, 'little')
        prog += self.entry_point.to_bytes(4, 'little')
        
        # program itself
        prog += self.bytecode
        prog += self.string_buffer
        prog += self.buffer

        return prog

    def save(self, filename: str):
        with open(filename, 'wb') as f:
            f.write(self.generate())
            
        print(f"Program saved to {filename}")