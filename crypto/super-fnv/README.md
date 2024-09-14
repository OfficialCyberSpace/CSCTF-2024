# super-fnv

There are multiple solutions for cc, so small combinations of the LLL reduced lattice had to be searched.

As an alternative, the 'FindInstance' function in Mathematica/Wolframscript is actually very well suited for this, you can see solve.py wrapper attached.

<br>

After the CTF ended Blupper updated his repo with branch-and-bound with PPL, I recommend you check it out!!!

<https://github.com/TheBlupper/linineq>

```python
from pwn import xor
from hashlib import sha256
load('https://raw.githubusercontent.com/TheBlupper/linineq/main/linineq.py')


enc = bytes.fromhex('4ba8d3d47b0d72c05004ffd937e85408149e13d13629cd00d5bf6f4cb62cf4ca399ea9e20e4227935c08f3d567bc00091f9b15d53e7bca549a')
tgt = 2957389613700331996448340985096297715468636843830320883588385773066604991028024933733915453111620652760300119808279193798449958850518105887385562556980710950886428083819728334367280
x = 2093485720398457109348571098457098347250982735
k = 1023847102938470123847102938470198347092184702
mod = 2**600
n = 9
M = matrix([[k**(n - i) for i in range(n)]])
lb = [-2**67]*n
ub = [2**67]*n

for cc in solve_bounded_mod_gen(M, [tgt - x*k**n], lb, ub, mod):
    key = sha256("".join(str(i) for i in cc).encode()).digest()
    flag = xor(enc, key)
    if b"CSCTF" in flag:
        print(flag)
        break
```
