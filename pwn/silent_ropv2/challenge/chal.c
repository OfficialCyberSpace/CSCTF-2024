#include <stdio.h>

int init(){
    setvbuf(stdin,0x0,2,0);
    fclose(stdout);
    return;
}

int vuln(){
    char vulnbuf[16];
    read(0,&vulnbuf,0x400);

    return;
}

int gift(){
    asm("pop rdx;");
    asm("ret;");
    asm("nop;");
    asm("mov [rdi],rdx");
    asm("ret;");
    asm("mov rdi,[rdx]");
    asm("ret;");
    asm("mov [rdx + rsi],rdi");
    asm("ret;");
    asm("mov rdx,rdi;");
    asm("ret;");
    asm("add rdi,rdx;");
    asm("ret;");
    asm("mov [rsp + rdx],rdi;");
    asm("ret;");
}


int main(){
    init();
    vuln();
    
    return 0;
}