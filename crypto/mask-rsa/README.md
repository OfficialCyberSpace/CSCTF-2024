# mask-rsa

|              |                                                                                    |
| ------------ | ---------------------------------------------------------------------------------- |
| **CTF**      | [Cyberspace CTF](https://2024.csc.tf/) [(CTFtime)](https://ctftime.org/event/2428) |
| **Author**   | aa.crypto                                                                          |
| **Category** | crypto                                                                             |
| **Solves**   | 6                                                                                  |

# Solution

we are given `e = 3`

`513-bit` primes must have 155 digits

`p * q = n` must be of 309 digits

we are given the result of RSA encryption of our own expression in terms of arithmetic operations of `p` and `q` but with alternate digits only

take this as an example

```
p = 24684648247466269511862357492704507147026946308415554076071325126890930007019654858728204224726147599743830015323289763883512220043753711112531755720047301
q = 26079186402474507123334783297583297354382920750787253497548250716839470583806962555902947182280722601358197870260046062048224750203714493530675129397377871
n = 643755542925188508237864190744989138238809598971443208599145655227366855638040406488967576526958041168869445702603937739133986690472525494291504254142120584102912553184555027574207328779371992990590946852660876782685325339542936824672739314430976487627186216213587374515049934150935412812892852201297490676171
```

from the chall we could get

```
pow(p, e, n)      # input "p"
pow(-p, e, n)     # input "-p"
pow(q, e, n)      # input "q"
pow(-q, e, n)     # input "-q"
pow(2*p, e, n)    # input "p+p"
pow(-2*p, e, n)   # input "-p-p"
pow(2*q, e, n)    # input "q+q"
pow(-2*q, e, n)   # input "-q-q"
pow(p+q, e, n)    # input "p+q"
pow(-(p+q), e, n) # input "-p-q"
pow(p-q, e, n)    # input "p-q"
pow(q-p, e, n)    # input "q-p"
pow(p*p, e, n)    # input "p*p"
pow(-p*p, e, n)   # input "-p*p"
pow(q*q, e, n)    # input "q*q"
pow(-q*q, e, n)   # input "-q*q"
```

308-digit case

```
pow(p, e, n)   =  71943556801598728594840149234569310988208493755926233291563315987719861740985377231703315350517132557905377397274430552423583026772678726538833198609271594151214322607155605827439675881779920952889542855791634487188064698073937328952879459405099341717340004180200013900442452042289944999469377326450642504042
what we get is:  '7_9_3_5_8_1_9_7_8_9_8_0_4_2_4_6_3_0_8_2_8_9_7_5_2_2_3_9_5_3_1_9_7_1_8_1_4_9_5_7_2_1_0_3_5_5_5_7_3_5_7_0_3_7_9_2_4_3_5_2_2_5_3_2_7_2_7_7_6_3_8_3_9_6_9_7_5_4_5_2_4_2_6_7_5_6_5_2_4_9_7_8_1_7_9_0_5_8_9_4_8_5_9_6_4_8_1_8_6_6_8_7_9_7_2_9_2_7_4_9_0_0_9_4_7_7_4_0_4_8_2_0_1_9_0_4_4_2_4_2_9_4_9_9_6_3_7_2_4_0_4_5_4_4_'
```

309-digit case

```
pow(-p, e, n) =  571811986123589779643024041510419827250601105215516975307582339239646993897055029257264261176440908610964068305329507186710403663699846767752671055532848989951698230577399421746767652897592072037701403996869242295497260641468999495719859855025877145909846212033387360614607482108645467813423474874846848172129
what we get is: '5_1_1_9_6_2_5_9_7_6_3_2_0_1_1_4_9_2_2_0_0_1_5_1_5_6_7_3_7_8_3_9_3_6_6_9_8_7_5_0_9_5_2_4_6_1_6_4_9_8_1_9_4_6_3_5_2_5_7_8_7_0_0_6_3_9_8_6_6_7_2_7_0_5_3_8_8_8_9_1_9_2_0_7_3_9_2_7_6_6_6_2_9_5_2_7_0_7_0_4_3_9_8_9_4_2_5_9_2_0_4_4_8_9_4_5_1_8_9_5_0_5_7_1_5_0_8_6_1_0_3_8_3_0_1_6_7_8_1_8_4_4_7_1_4_3_7_8_4_4_8_8_7_1_9'
```

notice the above pairs sum up to `n` with the added negative sign, so, if the original and negative one are both 309-digit,

```
pow(p+q, e, n)
1_3_2_8_5_4_2_8_5_3_5_4_3_3_4_4_1_2_8_6_0_0_3_2_8_0_5_6_4_2_3_8_6_4_4_2_7_9_0_1_2_1_5_9_6_2_6_7_8_7_6_4_3_5_0_7_6_7_5_1_7_3_5_7_6_0_8_0_7_8_9_5_4_4_8_4_3_3_4_6_9_6_7_2_3_8_1_9_8_0_1_3_8_0_9_2_4_1_6_1_5_3_6_1_4_3_7_9_3_4_6_9_4_9_1_7_1_1_3_9_1_5_5_5_4_3_1_1_6_5_4_7_1_9_2_2_3_7_4_3_1_5_9_7_8_6_7_2_7_2_0_3_1_6_2
pow(-p-q, e, n)
4_9_2_6_6_7_9_9_5_8_2_1_8_6_9_5_8_1_3_1_0_5_5_4_6_2_5_9_5_1_2_6_6_9_2_2_8_8_3_2_3_7_4_7_0_2_0_8_2_3_0_3_5_9_6_4_3_1_2_2_3_0_3_9_4_6_7_4_2_4_2_5_8_9_5_6_7_5_6_6_1_8_5_5_1_6_1_6_5_0_1_5_9_2_2_6_5_8_2_7_1_1_0_8_2_4_5_8_9_1_7_5_8_4_6_7_6_5_5_2_2_5_1_9_2_8_0_4_5_6_9_1_2_5_8_7_6_5_6_7_2_8_3_4_9_6_7_9_4_7_3_7_6_5_9
```

we can get possible digits candidates by adding them, but there are 2 possible candidates for each digit -- first digit of `n` is either 5 or 6, and 3rd are 2 or 3, etc.

We can get other pairs with this pattern so we could narrow down some digit position and know the exact digit (well we actually don't need this, 1 pair is enough, it doesn't matter to have 2 candidates for every digit)

```
pow(q*q, e, n)
3_3_1_5_0_5_5_0_7_2_0_2_2_1_7_2_3_9_5_5_6_6_1_8_5_9_6_8_9_9_0_2_0_6_5_2_7_0_2_4_7_5_7_7_9_7_1_7_7_3_7_3_9_6_8_8_6_5_1_4_2_7_4_2_2_9_4_6_3_3_6_7_1_7_2_9_8_4_7_3_1_4_5_7_1_8_5_3_1_8_9_0_3_1_8_8_6_6_0_5_7_3_6_7_5_0_9_8_3_5_9_0_0_1_7_5_2_1_8_6_6_3_9_4_1_7_4_4_3_3_3_4_5_0_7_0_4_1_7_3_5_6_3_9_2_2_1_1_6_9_4_1_7_2_0
pow(-q*q, e, n)
2_0_3_0_2_7_6_8_3_0_7_3_9_9_7_7_5_4_6_3_4_9_7_8_9_3_4_7_9_4_6_3_2_7_1_2_8_7_1_9_9_3_2_9_8_8_4_8_2_7_9_5_0_8_8_3_4_3_5_8_8_6_4_4_8_7_0_9_5_9_4_2_1_7_1_1_2_3_3_9_0_1_7_1_3_6_6_2_3_2_4_7_4_2_3_1_3_4_8_3_9_2_0_3_2_7_3_0_9_9_4_5_2_1_0_9_4_5_0_4_8_7_7_0_5_5_7_1_7_8_9_4_8_4_4_0_5_1_3_7_8_7_9_1_6_0_3_0_4_9_0_8_9_9_1
```

we know the 3rd digit of `n` is 3 now. The possible candidates of digits of `n` are as follows, for convenience mapping with the code, i am putting the Least Sig Digit as the first element of the array.

Also recall the Least sig Digit of `n` must be odd.

```
n:
309-th digit: [1],   # Least Sig digit of n, must be 1 but not 2
308-th digit: unknown,
307-th digit: [1, 2],
306-th digit: unknown,
305-th digit: [7],   # since there was 6 and 7 from the above results, we know it must be 7
304-th digit: unknown
303-rd digit: [0],
...
...
...
3rd    digit: [3],
2nd    digit: unknown,
1st    digit: [5, 6],   # Most Sig digit
```

With this info of `n`, now we work with the fact that
`pow(p, e, n) * 8 = pow(2p, e, n)` since `e = 3`

```
pow(p, e, n)   # 308 digits
 7_9_3_5_8_1_9_7_8_9_8_0_4_2_4_6_3_0_8_2_8_9_7_5_2_2_3_9_5_3_1_9_7_1_8_1_4_9_5_7_2_1_0_3_5_5_5_7_3_5_7_0_3_7_9_2_4_3_5_2_2_5_3_2_7_2_7_7_6_3_8_3_9_6_9_7_5_4_5_2_4_2_6_7_5_6_5_2_4_9_7_8_1_7_9_0_5_8_9_4_8_5_9_6_4_8_1_8_6_6_8_7_9_7_2_9_2_7_4_9_0_0_9_4_7_7_4_0_4_8_2_0_1_9_0_4_4_2_4_2_9_4_9_9_6_3_7_2_4_0_4_5_4_4_

pow(2p, e, n)  # 309 digits
5_5_4_4_4_1_7_9_2_7_8_2_1_3_7_5_4_8_9_5_6_9_0_4_4_9_6_3_2_0_5_7_0_7_8_9_9_7_8_0_7_5_6_6_2_8_4_3_0_0_6_2_3_1_1_8_9_4_4_1_3_8_6_2_4_8_4_9_1_3_0_6_5_8_7_1_2_5_2_9_1_5_0_5_2_4_4_6_9_1_4_7_5_2_9_6_6_3_1_3_2_4_3_3_7_8_7_0_5_7_8_5_1_9_6_1_2_0_5_7_2_0_9_7_3_3_7_0_3_4_1_0_1_1_0_5_9_1_3_8_1_5_9_9_7_5_1_6_1_0_1_0_3_3_6

pow(-p, e, n)  # 309 digits
5_1_1_9_6_2_5_9_7_6_3_2_0_1_1_4_9_2_2_0_0_1_5_1_5_6_7_3_7_8_3_9_3_6_6_9_8_7_5_0_9_5_2_4_6_1_6_4_9_8_1_9_4_6_3_5_2_5_7_8_7_0_0_6_3_9_8_6_6_7_2_7_0_5_3_8_8_8_9_1_9_2_0_7_3_9_2_7_6_6_6_2_9_5_2_7_0_7_0_4_3_9_8_9_4_2_5_9_2_0_4_4_8_9_4_5_1_8_9_5_0_5_7_1_5_0_8_6_1_0_3_8_3_0_1_6_7_8_1_8_4_4_7_1_4_3_7_8_4_4_8_8_7_1_9
```

we can work from Least Sig Digit to recover all unknown digits, i take the final digits to illustrate

```
4_0_4_5_4_4_       ...(a): pow(p, e, n)

x          8
____________

_0_1_0_3_3_6       ...(b): pow(2p, e, n)
```

and recall `pow(p, e, n) + pow(-p, e, n) = n`
final digits of `pow(-p, e, n)` is:

```
    _4_8_8_7_1_9   ...(c): pow(-p, e, n)

+   4_0_4_5_4_4_   ...(a): pow(p, e, n)
________________

         0_7_1_1   ... n
             or
             2
```

e.g. last digit of `(a)` could be `2` or `7` to satisty `(a) * 8 = (b)`, but since `(a) + (c) == n`, it has to be `2`, then we keep on recover each digit of `(a)` and `(b)` from Least Sig digit, even if there could be 2 candidates for `n`, there will still be 1 unique solution

we now solved

```
pow(p, e, n) =   # 308 digits
71943556801598728594840149234569310988208493755926233291563315987719861740985377231703315350517132557905377397274430552423583026772678726538833198609271594151214322607155605827439675881779920952889542855791634487188064698073937328952879459405099341717340004180200013900442452042289944999469377326450642504042
pow(2p, e, n) =  # 309 digits
575548454412789828758721193876554487905667950047409866332506527901758893927883017853626522804137060463243019178195444419388664214181429812310665588874172753209714580857244846619517407054239367623116342846333075897504517584591498631623035675240794733738720033441600111203539616338319559995755018611605140032336
```

The question is: how do we get this scenario where `pow(p, e, n)` is 308 digits?

Answer: just loop until we get `mask_expr('p')` or `mask_expr('-p')` is of 154 digits (or else normally its 155). And to help solving the chall we further require `pow(-2p, e, n)` to be 308 digits, to see why:

Because we can compute all the digits of `n` from least sig digit by the following 2 equations

1. `pow(2p, e, n) + pow(-2p, e, n) == n`
2. `pow(p, e, n) + pow(-p, e, n) == n`

```
   ...605140032336     # pow(2p, e, n)
+  _8_6_2_5_6_3_3_     # pow(-2p, e, n), 308 digits
==================
   ..............1

   8_4_4_8_8_7_1_9     # pow(-p, e, n)
+  326450642504042     # pow(p, e, n)
==================
```

1. from `pow(2p, e, n)` pair, starting from ending digit `1`, we know the 2nd digit is `7`
2. then from `pow(p, e, n) pair`, we know the 3rd digit is `1`
3. alternating between the 2 we can solve for `n`, finally get `p` by `gcd(n, pow(p, e, n))`, and the rest is basic RSA