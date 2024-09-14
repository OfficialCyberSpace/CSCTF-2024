section .bss
    buffer resb 64

section .text
    global _start

_start:
    call main

end:
    mov rax, 60
    xor rdi, rdi
    syscall

main:
    push rbp
    mov rbp, rsp
    sub rsp, 64

    mov rdx, 80
    mov rdi, 0
    lea rsi, [rbp-64]
    mov rax, 0
    syscall

    leave
    ret

_:
    movzx rdi, byte [rsi]
    ret