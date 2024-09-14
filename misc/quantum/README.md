# Quantum

|              |                                                                                    |
| ------------ | ---------------------------------------------------------------------------------- |
| **CTF**      | [Cyberspace CTF](https://play.csc.tf/) [(CTFtime)](https://ctftime.org/event/2428) |
| **Author**   | [nullchilly](https://github.com/nullchilly)                                        |
| **Category** | Misc                                                                               |
| **Solves**   | 6 / 830                                                                            |
| **Files**    | [server.py](challenge/server.py) [quantum-dist.py](challenge/quantum-dist.py)      |

# Solution

First you need to solve the challenge with 2n ask queries

## For ask

```py
def ask(x0, y0):
    sum = 0
    for x, y in p:
        sum += abs(x - x0) + abs(y - y0)
    return sum
```

Let `S = ask` we have:

```
S(x0, y0) = Σ_(x, y) ∈ P {|x - x0| + |y - y0|}
S(x0, y0) = Σ_(x, y) ∈ P {(|x - x0| + |y|) + (|x| + |y - y0|) - (|x| + |y|)}
= Σ_(x, y) ∈ P {|x - x0| + |y|} + Σ_(x, y) ∈ P {|x| + |y - y0|} - Σ_(x, y) ∈ P {|x| + |y|}
= S(x, 0) + S(0, y) - S(0, 0)
```

Then ask all for `x ∈ [0, n) S(x, 0)` and for all `y ∈ [0, n) S(0, y)`
You now have the answer of `S(x, y)` for all `x, y` after 2n queries

```py
def ask(x0, y0):
    return S(x0, 0) + S(0, y0) - S(0, 0)
```

## For query:

```
Σ_x ∈ [x0, x1] Σ_y ∈ [y0, y1] S(x, y)
= Σ_x ∈ [x0, x1] {(y1 - y0 + 1) * S(x, 0)}
+ Σ_y ∈ [y0, y1] {(x1 - x0 + 1) * S(0, y)}
- (x1 - x0 + 1) * (y1 - y0 + 1) * S(0, 0)
```

Can easily be done in O(1) using prefix sum

```py
def query(x0, y0, x1, y1):
    return (
        (pSx[x1] - pSx[x0 - 1]) * (y1 - y0 + 1)
        + (x1 - x0 + 1) * (pSy[y1] - pSy[y0 - 1])
        - (x1 - x0 + 1) * (y1 - y0 + 1) * S(0, 0)
    )
```

You can refer to [quantum.py](./challenge/quantum.py) to see how we implement these functions remotely

## For 1.9n asks

This is only possible thanks to the help of [Aeren](https://github.com/Aeren1564). Thank you so much!!

Query all even positions -> for each odd positions, if the 3 even numbers around it are colinear, try to determines the value at that position, otherwise you query it

Refer to [solve.py](solve.py) for the implementation

There are also an interesting solutions by participants:

### By white

Basically the only optimization I did is first send every other point then if the change between 3 points I sent are same then we know the points in the middle has the same difference
or well half the difference
Then we run it a few times until we get a good rng on remote

Refer to [solve_white.py](./solve_white.py) for their implementation

### By [mfornet](https://github.com/mfornet)

[1]: You don't need to recover the points, it is enough to recover how many points have x coordinate for each x, and similarly how many points have y coordinate for each y. With this information we can answer the queries efficiently.

Let f(x) := ask(x, 0) [It will be symmetric for y]

[2]: If you ask f(x) and (x + 1) you can deduce how many points have coordinate less or equal than `x` and how many have coordinates greater or equal than `x + 1`.

```
LEFT = (f(x + 1) - f(x) + n) / 2
RIGHT = n - LEFT
```

Due to [1] we only need to recover for each `x`, how many points has this coordinate.

[3]: For n >= 450, there will be several `x` with frequency 0. I was empirically testing this, didn't went deep into expected values.

[4]: If we know `f(i)` and `f(i+1)`, if frequency at `i+1` and frequency at `i+2` is zero (there are no points with these coordinates) we can deduce the value at `f(i + 3)`.

```
f(i+3) = 3 * (LEFT - RIGHT) + f(i)
```

[5]: Moreover, [4] can be generalized to arbitrary distances. If you know `f(i)` and `f(i+1)`, and frequency at all `j` such that `i < j < i + d` is zero, then we can compute `f(i + d)`.

```
f(i+d) = d * (LEFT - RIGHT) + f(i)
```

[6]: Without proof, I assumed that [4] (and [5]) is not only sufficient, but also necessary. Meaning, that if we ask for f(i+d), and we compute what is the value we are expecting given frequency at intermediate values is zero, they will only match if the values are actually 0.

---

With this observations we can compute `f(i)`, `f(i+1)` and using [5] and [6] we can try to find how many frequencies are zero without asking for all of them. We start asking for `f(i+3)`, then `f(i+5)`, and so on `f(i+2k+1)`, until we find something that is non zero.

I'm attaching the python code I used to check (empirically) the number of queries required.

```py
from random import randint


def main():
    # The bigger `n` is, less questions we need to ask
    # 450 is the smallest value that n can take.
    n = 450

    xs = set([randint(1, n) for _ in range(n)])
    queries = set()

    i = 0
    while i < n:
        if i + 3 >= n:
            # The last 3 elements are asked separately
            for j in range(i, n):
                queries.add(j)
            break

        queries.add(i)
        queries.add(i + 1)

        j = i + 3
        while j < n:
            queries.add(j)

            if j - 1 in xs or j - 2 in xs:
                # There are points at j - 1 or j - 2, so we need to ask for them.
                i = j - 1
                break

            # Yay, we don't need to ask for `j - 1`.

            j += 2
            i = j

    # Multiplying by 2 is ok, because we repeat this in both dimensions, and they are independent.
    print(2 * len(queries) / n)
```
