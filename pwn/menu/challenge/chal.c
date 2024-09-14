#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <seccomp.h>
#include <syscall.h>

void sandbox(){
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_ALLOW);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(open), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(clone), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(fork), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(vfork), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(ptrace), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(close), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(mmap), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(munmap), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(nanosleep), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(kill), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(openat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(sendfile), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pwrite64), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pwritev), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pwritev2), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(writev), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(process_vm_writev), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pread64), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(preadv), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(preadv2), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(readv), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(process_vm_readv), 0);

  seccomp_load(ctx);
  return;
}

void init_proc(){
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  sandbox();
}

void red() {
  printf("\033[1;31m");
}

void blue() {
  printf("\033[0;34m");
}

void reset() {
  printf("\033[0m");
}

void greeting(){
  red();
  puts("   _____             __     __           _____                   __  __     ___  ");
  puts("  / ____|            \\ \\   / /          |  __ \\                 |  \\/  |   |__ \\ ");
  puts(" | |     __ _ _ __    \\ \\_/ /__  _   _  | |__) |_      ___ __   | \\  / | ___  ) |");
  puts(" | |    / _` | '_ \\    \\   / _ \\| | | | |  ___/\\ \\ /\\ / / '_ \\  | |\\/| |/ _ \\/ / ");
  puts(" | |___| (_| | | | |    | | (_) | |_| | | |     \\ V  V /| | | | | |  | |  __/_|  ");
  puts("  \\_____\\__,_|_| |_|    |_|\\___/ \\__,_| |_|      \\_/\\_/ |_| |_| |_|  |_|\\___(_)  ");
  reset();
  puts("Welcome!");
  puts("Can you pwn the menu?");
  puts("Just a little gift: ");
  blue();
  printf("%p\n", &greeting);
  reset();
}

void menu(){
  char menu[200];
  puts("\nWelcome to the menu\nIt's not a heap chall!");
  printf("What do you want to order today?\n");
  read(0, menu, 2000);
  puts("Thank you for your order!");
  puts("Your order is on its way!");
}

int main(){
  init_proc();
  greeting();
  menu();
  return 0;
}