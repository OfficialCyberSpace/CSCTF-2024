# Connorsmith

<https://cryptohack.gitbook.io/cryptobook/untitled/low-private-component-attacks/boneh-durfee-attack>

It is an adaption of this attack, where you can use the partial p+q as an additional hint.

$$1 \equiv e \cdot d \ \ (\text{mod } \phi(N))$$

$$1 + k \cdot \phi(N) = e \cdot d$$

Now work mod e:

$$1 + k \cdot \phi(N) \equiv 0 \ \ (\text{mod }e)$$

Let x = 2k:

$$1 + \frac{x \cdot \phi(N)}{2} \equiv 0 \ \ (\text{mod }e)$$

$$1 + \frac{x \cdot (N+1-(p+q)))}{2} \equiv 0 \ \ (\text{mod }e)$$

Then using the hint, we have

$$p+q = \text{hint}\cdot2^{795} + y$$

$$1 + \frac{x \cdot (N+1-(\text{hint}\cdot2^{795} + y)))}{2} \equiv 0 \ \ (\text{mod }e)$$

And now it is bivariate coppersmith to solve the 2 unknowns x and y.

For bivariate in particular, the resultant integer solver is generally best.

The exact bound for y is `2**795` which we can see in the code.

```python
d = randint(0, int(N**0.35))
```

The upper bound for x is `e**0.35`, but we may want to bruteforce some slightly lower bounds for better results when doing Coppersmith (otherwise it is more difficult, you may need bigger lattice dimensions or it may not work at all).

Then it's a matter of trial and error for tweaking the bound for x or the lattice dimensions m and d.

2 examples that work:

```python
roots = bivariate(f, bounds=(2**(ZZ(e**0.35).nbits() - 2), 2**b), m=5, d=3) # tighter bound for x and lower m
roots = bivariate(f, bounds=(ZZ(e**0.35), 2**b), m=6, d=3) # looser bound for x but bigger m
```

2 multivariate Coppersmith repos you could use:

<https://github.com/josephsurin/lattice-based-cryptanalysis/blob/main/lbc_toolkit/problems/small_roots.sage>

<https://github.com/kionactf/coppersmith>
