#include <stdio.h>
#include <sys/mman.h>

void init(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    init();
    puts("Welcome to my shellcode tester!\n");
    puts("This time in a different architecture");
    puts("Just give me a shellcode and I will run it in a safe place!");
    
    char *shellcode;

    shellcode = mmap((void *)NULL, 1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    read(0, shellcode, 1000);
    (*(void(*)()) shellcode)();

    return 0;
}