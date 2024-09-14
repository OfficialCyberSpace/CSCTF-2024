#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define NUM_REGISTERS 8
#define STACK_SIZE 1024

typedef struct _VmInfo {
    uint8_t* data;
    uint32_t len;
    uint32_t entrypoint;
    uint32_t registers[NUM_REGISTERS];
    uint32_t stack[STACK_SIZE];
    uint32_t sp;
    uint32_t pc;
    bool zf;
} VmInfo;

enum {
    VM_MOV_RR,
    VM_MOV_RC,
    VM_ADD_RR,
    VM_ADD_RC,
    VM_SUB_RR,
    VM_SUB_RC,
    VM_MUL_RR,
    VM_MUL_RC,
    VM_DIV_RR,
    VM_DIV_RC,
    VM_XOR_RR,
    VM_XOR_RC,
    VM_AND_RR,
    VM_AND_RC,
    VM_JMP_R,
    VM_JMP_C,
    VM_JZ,
    VM_JNZ,
    VM_CALL,
    VM_RET,
    VM_PUSH,
    VM_POP,
    VM_CMP_RR,
    VM_CMP_RC,
    VM_STORE_RR,
    VM_STORE_RC,
    VM_LOAD_RR,
    VM_LOAD_RC,
    VM_READ_BYTE,
    VM_PRINT_STR,
    VM_HALT
};

void vm_mov_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->registers[reg1] = vm->registers[reg2];
    vm->pc += 3;
}

void vm_mov_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    vm->registers[reg] = constant;
    vm->pc += 6;
}

void vm_add_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->registers[reg1] += vm->registers[reg2];
    vm->zf = (vm->registers[reg1] == 0);
    vm->pc += 3;
}

void vm_add_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    vm->registers[reg] += constant;
    vm->zf = (vm->registers[reg] == 0);
    vm->pc += 6;
}

void vm_sub_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->registers[reg1] -= vm->registers[reg2];
    vm->zf = (vm->registers[reg1] == 0);
    vm->pc += 3;
}

void vm_sub_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    vm->registers[reg] -= constant;
    vm->zf = (vm->registers[reg] == 0);
    vm->pc += 6;
}

void vm_mul_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->registers[reg1] *= vm->registers[reg2];
    vm->zf = (vm->registers[reg1] == 0);
    vm->pc += 3;
}

void vm_mul_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    vm->registers[reg] *= constant;
    vm->zf = (vm->registers[reg] == 0);
    vm->pc += 6;
}

void vm_div_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    if (vm->registers[reg2] != 0) {
        vm->registers[reg1] /= vm->registers[reg2];
        vm->zf = (vm->registers[reg1] == 0);
    } else {
        printf("Error: Division by zero\n");
        exit(1);
    }
    vm->pc += 3;
}

void vm_div_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    if (constant != 0) {
        vm->registers[reg] /= constant;
        vm->zf = (vm->registers[reg] == 0);
    } else {
        printf("Error: Division by zero\n");
        exit(1);
    }
    vm->pc += 6;
}

void vm_xor_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->registers[reg1] ^= vm->registers[reg2];
    vm->zf = (vm->registers[reg1] == 0);
    vm->pc += 3;
}

void vm_xor_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    vm->registers[reg] ^= constant;
    vm->zf = (vm->registers[reg] == 0);
    vm->pc += 6;
}

void vm_and_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->registers[reg1] &= vm->registers[reg2];
    vm->zf = (vm->registers[reg1] == 0);
    vm->pc += 3;
}

void vm_and_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    vm->registers[reg] &= constant;
    vm->zf = (vm->registers[reg] == 0);
    vm->pc += 6;
}

void vm_jmp_r(VmInfo* vm, uint8_t reg) {
    vm->pc = vm->registers[reg];
}

void vm_jmp_c(VmInfo* vm, uint32_t addr) {
    vm->pc = addr;
}

void vm_jz(VmInfo* vm, uint32_t addr) {
    if (vm->zf) {
        vm->pc = addr;
    } else {
        vm->pc += 5;
    }
}

void vm_jnz(VmInfo* vm, uint32_t addr) {
    if (!vm->zf) {
        vm->pc = addr;
    } else {
        vm->pc += 5;
    }
}

void vm_call(VmInfo* vm, uint32_t addr) {
    vm->stack[vm->sp++] = vm->pc + 5;
    vm->pc = addr;
}

void vm_ret(VmInfo* vm) {
    vm->pc = vm->stack[--vm->sp];
}

void vm_push(VmInfo* vm, uint8_t reg) {
    vm->stack[vm->sp++] = vm->registers[reg];
    vm->pc += 2;
}

void vm_pop(VmInfo* vm, uint8_t reg) {
    vm->registers[reg] = vm->stack[--vm->sp];
    vm->pc += 2;
}

void vm_cmp_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->zf = (vm->registers[reg1] == vm->registers[reg2]);
    vm->pc += 3;
}

void vm_cmp_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    vm->zf = (vm->registers[reg] == constant);
    vm->pc += 6;
}

void vm_store_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    *((uint32_t*)&vm->data[vm->registers[reg1]]) = vm->registers[reg2];
    vm->pc += 3;
}

void vm_store_rc(VmInfo* vm, uint8_t reg, uint32_t constant) {
    *((uint32_t*)&vm->data[vm->registers[reg]]) = constant;
    vm->pc += 6;
}

void vm_load_rr(VmInfo* vm, uint8_t reg1, uint8_t reg2) {
    vm->registers[reg1] = *((uint32_t*)&vm->data[vm->registers[reg2]]);
    vm->pc += 3;
}

void vm_load_rc(VmInfo* vm, uint8_t reg, uint32_t addr) {
    vm->registers[reg] = *((uint32_t*)&vm->data[addr]);
    vm->pc += 6;
}

__attribute__((always_inline)) void vm_read_byte(VmInfo* vm, uint8_t reg) {
    int ch = getchar();
    if (ch == EOF) {
        vm->registers[reg] = 0;
    } else {
        vm->registers[reg] = (uint8_t)ch;
    }
    vm->pc += 2;
}

__attribute__((always_inline)) void vm_print_str(VmInfo* vm, uint32_t addr) {
    printf("%s", &vm->data[addr]);
    fflush(stdout);
    vm->pc += 5;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s [file]\n", argv[0]);
        return 1;
    }

    FILE* fp = fopen(argv[1], "rb");
    if (!fp) {
        printf("Failed to open %s\n", argv[1]);
        return 1;
    }

    VmInfo vm = {0};
    fread(&vm.len, 4, 1, fp);
    fread(&vm.entrypoint, 4, 1, fp);
    // printf("len: %#x\nentry: %#x\n", vm.len, vm.entrypoint);

    vm.data = (uint8_t*)malloc(vm.len);
    fread(vm.data, 1, vm.len, fp);
    fclose(fp);

    vm.pc = vm.entrypoint;
    vm.sp = 0;

    while (true) {
        uint8_t opcode = vm.data[vm.pc];
        switch (opcode) {
            case VM_MOV_RR:
                vm_mov_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_MOV_RC:
                vm_mov_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_ADD_RR:
                vm_add_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_ADD_RC:
                vm_add_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_SUB_RR:
                vm_sub_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_SUB_RC:
                vm_sub_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_MUL_RR:
                vm_mul_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_MUL_RC:
                vm_mul_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_DIV_RR:
                vm_div_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_DIV_RC:
                vm_div_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_XOR_RR:
                vm_xor_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_XOR_RC:
                vm_xor_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_AND_RR:
                vm_and_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_AND_RC:
                vm_and_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_JMP_R:
                vm_jmp_r(&vm, vm.data[vm.pc + 1]);
                break;
            case VM_JMP_C:
                vm_jmp_c(&vm, *((uint32_t*)&vm.data[vm.pc + 1]));
                break;
            case VM_JZ:
                vm_jz(&vm, *((uint32_t*)&vm.data[vm.pc + 1]));
                break;
            case VM_JNZ:
                vm_jnz(&vm, *((uint32_t*)&vm.data[vm.pc + 1]));
                break;
            case VM_CALL:
                vm_call(&vm, *((uint32_t*)&vm.data[vm.pc + 1]));
                break;
            case VM_RET:
                vm_ret(&vm);
                break;
            case VM_PUSH:
                vm_push(&vm, vm.data[vm.pc + 1]);
                break;
            case VM_POP:
                vm_pop(&vm, vm.data[vm.pc + 1]);
                break;
            case VM_CMP_RR:
                vm_cmp_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_CMP_RC:
                vm_cmp_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_STORE_RR:
                vm_store_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_STORE_RC:
                vm_store_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_LOAD_RR:
                vm_load_rr(&vm, vm.data[vm.pc + 1], vm.data[vm.pc + 2]);
                break;
            case VM_LOAD_RC:
                vm_load_rc(&vm, vm.data[vm.pc + 1], *((uint32_t*)&vm.data[vm.pc + 2]));
                break;
            case VM_READ_BYTE:
                vm_read_byte(&vm, vm.data[vm.pc + 1]);
                break;
            case VM_PRINT_STR:
                vm_print_str(&vm, *((uint32_t*)&vm.data[vm.pc + 1]));
                break;
            case VM_HALT:
                printf("Program halted\n");
                free(vm.data);
                return 0;
            default:
                printf("Unknown opcode: %d\n", opcode);
                free(vm.data);
                return 1;
        }
    }

    return 0;
}