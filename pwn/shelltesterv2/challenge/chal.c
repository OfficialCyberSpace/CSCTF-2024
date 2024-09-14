#include <stdio.h>

void gift() {
  system();
}

void vuln() {
  char buffer[50];
  char buf[100];

  printf("Tell me something: \n");
  fgets(buffer, 50, stdin);
  printf(buffer);
  printf("Do you want to say something before you leave?\n");
  fgets(buf, 1000, stdin);
}

int main() {
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);
  printf("Again an easy pwn, but now on a different architecture. Good Luck!\n");
  vuln();
  return 0;
}
