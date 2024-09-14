# Modulus RSA

|              |                                                                                    |
| ------------ | ---------------------------------------------------------------------------------- |
| **CTF**      | [Cyberspace CTF](https://2024.csc.tf/) [(CTFtime)](https://ctftime.org/event/2428) |
| **Author**   | aa.crypto                                                                          |
| **Category** | beginner, crypto                                                                   |
| **Solves**   | 109                                                                                |

# Solution

```
w = 115017953136750842312826274882950615840
x = 16700949197226085826583888467555942943
y = 20681722155136911131278141581010571320
c = 2246028367836066762231325616808997113924108877001369440213213182152044731534905739635043920048066680458409222434813
```

we are given `w = q % p`, `x = r % p` and `y = r % q`. Assume

```
q = i*p + w   ... (1)
r = j*p + x   ... (2)
r = k*q + y   ... (3)
```

TLDR: since the smallest prime `p` > `w` which is 127 bits. By simple division, the quotient between pairs of p,q,r must be `<= 3`. One can simply brute force all quotients (`i`, `j` and `k`) for `1` or `2` or `3` and solve the system of linear equations.

## Detailed Calculation

We know that all `p`, `q` and `r` are smaller than `1 << 128`, and we know all `i`, `j` and `k` are not 0 since `w`, `x` and `y` are not primes.

From `(1)`, we know `w < p`, so `1 << 128 > q = i*p + w > i*w + w = (i+1) * w`, `i` must be `1`.
From `(1)` again, `q = i*p + w = p + w > w + w = 2w`
From `(3)`, we know `1 << 128 > r = k*q + y > k*2w + y`, `k` must be `1`.

Assume `i = j = k = 1`, then `(1)`, `(2)`, `(3)` becomes

```
q = p + w    ... (4)
r = p + x    ... (5)
r = q + y    ... (6)
```

then, `(4) - (5) + (6)` gives `w - x + y = 0` which contradicts the given numbers. So `j != 1`.

From `(2)`, `1 << 128 > r = j*p + x > j*w + x`, so `j = 2`.

Now,

```
q = p + w
r = 2p + x
r = q + y
```

Solving these yield

```
p = y - x + w = 118998726094661667617520527996405244217
q = p + w = 234016679231412509930346802879355860057
r = q + y = 254698401386549421061624944460366431377
```

Applying the standard RSA decryption algorithm, we solve the flag

```
from Crypto.Util.number import long_to_bytes
n = p * q * r
d = pow(e, -1, (p-1)*(q-1)*(r-1))
m = long_to_bytes(pow(c, d, n))
```
