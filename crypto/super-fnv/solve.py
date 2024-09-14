from sage.all import *
from wolframclient.evaluation import WolframLanguageSession
from Crypto.Util.number import *
from wolframclient.language import wlexpr
from hashlib import sha256
session = WolframLanguageSession()
from tqdm import tqdm
from pwn import xor

def find_instances(xx, LB, UB, target, M, sol_cnt=1000):
    n = len(xx)
    expr = 'FindInstance[{'
    expr += '+'.join(f'{xx[i]}*x{i}' for i in range(n)) + f'+ k*{{{M}}} == {target}'
    expr += ','  + ','.join(f'x{i}<{UB},x{i}>{LB}' for i in range(n))
    expr += '},{' + ','.join(f'x{i}' for i in range(n)) + f',k}},Integers, {sol_cnt}]'
    for sol in tqdm(session.evaluate(wlexpr(expr))):
        yield [x[1] for x in sol[:-1]]

enc = bytes.fromhex('4ba8d3d47b0d72c05004ffd937e85408149e13d13629cd00d5bf6f4cb62cf4ca399ea9e20e4227935c08f3d567bc00091f9b15d53e7bca549a')
target = 2957389613700331996448340985096297715468636843830320883588385773066604991028024933733915453111620652760300119808279193798449958850518105887385562556980710950886428083819728334367280

def solve(target, n, sol_cnt=10_000):
    x = 2093485720398457109348571098457098347250982735
    k = 1023847102938470123847102938470198347092184702
    rets = []
    for cc in find_instances([k**(n - i) for i in range(n)], -2**67, 2**67, target - x*k**n, 2**600, sol_cnt=sol_cnt):
        key = sha256("".join(str(i) for i in cc).encode()).digest()
        flag = xor(enc, key)
        if b"CSCTF" in flag:
            print(flag)

solve(target, 9)
session.terminate()
