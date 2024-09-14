#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
// gcc chall.c -o byte-modification-service -no-pie

void init(){
	asm(
		"mov $0xa, %rax\n"
		"mov $0x401000, %rdi\n"
		"mov $0x1000, %rsi\n"
		"mov $7, %rdx\n"
		"syscall\n"
	);
	setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

int bye(){
	puts("Thanks for modifying the byte, goodbye.");
	exit(0);
	return 0;
}

int win(){
  FILE *f = fopen("flag.txt","r");
  char flag[50];

  if (f == NULL) {
    puts("flag.txt not found!");
    exit(0);
  }
  
  fgets(flag, 50, f);
  printf("%s\n", flag);
  puts("How could you do that?!");
  puts("That's my precious secret.");
  puts("Anyway congratulations");
  return 0;
}

int vuln(){
	char buf[32];
	int xor;  // -0x44
	int idx;  // -0x40
	char addr[8] = {0,0,0,0,0,0,0,0};
	int i;  // 0x3c
	puts("which stack position do you want to use?");
	scanf("%d", &i);
	i = i * 8;
	asm(
		"mov %rsp, %rdi\n"
		"mov -0x3c(%rbp), %eax\n"
		"add %rax, %rdi\n"
		"mov (%rdi), %rdx\n"
		"mov %rdx, -0x38(%rbp)\n"
	);
	//printf("%s", addr+1);
	puts("you have one chance to modify a byte by xor.");
	puts("Byte Index?");
	scanf("%d", &idx);
	if ( idx < 0 || idx > 7) {
		puts("don't cheat!");
		exit(0);
	}
	puts("xor with?");
	scanf("%d", &xor);
	asm(
		"mov %rbp, %rdi\n"
		"sub $0x38, %rdi\n"
		"mov -0x40(%rbp), %ebx\n"
		"mov -0x44(%rbp), %eax\n"
		"add %rbx, %rdi\n"
		"xorb %al, (%rdi)\n"
	);
	puts("finally, do you have any feedback? it will surely help us improve our service.");
	scanf("%20[^@]", buf);
	printf(buf);
	bye();
	return 0;
}

int main(){
	init();
	vuln();
	return 0;
}