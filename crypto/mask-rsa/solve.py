from math import gcd
from pwn import remote, context
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long

context.log_level = 'ERROR'

e = 3

def sum_coeff(arr):
    return sum([digit * 10 ** idx for idx, digit in enumerate(arr)])

def mask_expr(expr):
    global e, n
    global p, q
    assert len(expr) <= 4
    assert all([c in r'pqr+-*/%' for c in expr])
    res = eval(expr)
    return str(pow(res, e, n))[::2]

def construct_array(expr1, expr2):
    global io
    n_digit = 155
    io.sendlineafter(b'p, q and r: ', expr1.encode())
    mask1 = io.recvline().decode().strip()
    io.sendlineafter(b'p, q and r: ', expr2.encode())
    mask2 = io.recvline().decode().strip()

    # last element of array is LSB of the number
    arr1 = [None] * (n_digit * 2 - 1)
    arr2 = [None] * (n_digit * 2 - 1)

    # loose check here, we assume the result must be of either 309 or 308 digits
    # further check will be done later
    if len(mask1) == n_digit:
        offset = 0
    else:
        offset = 1

    for idx, digit in enumerate(mask1):
        arr1[idx * 2 + offset] = int(digit)

    if len(mask2) == n_digit:
        offset = 0
    else:
        offset = 1
    for idx, digit in enumerate(mask2):
        arr2[idx * 2 + offset] = int(digit)

    # first elements of arr1 and arr2 are least significant digit of the number
    return arr1[::-1], arr2[::-1], mask1, mask2

conf = {
    # name: (func, expr1, expr2)
    'p': (lambda p,q,r: p, 'p', '-p'),
    'q': (lambda p,q,r: q, 'q', '-q'),
    'p+q': (lambda p,q,r: p+q, 'p+q', '-p-q'),
    'p+p': (lambda p,q,r: p+q, 'p+p', '-p-p'),
    'q+q': (lambda p,q,r: p+q, 'q+q', '-q-q'),
    'pxq': (lambda p,q,r: p*q, 'p*q', '-p*q'),
    'pxp': (lambda p,q,r: p*q, 'p*p', '-p*p'),
    'qxq': (lambda p,q,r: p*q, 'q*q', '-q*q'),
    'p-q': (lambda p,q,r: q+r, 'p-q', 'q-p'),
}
valids = 0
for i in range(5000):
    if i % 10 == 0:
        print('i', i)
    io = remote('mask-rsa.challs.csc.tf', 1337)
    io.recvuntil(b'c = ')
    c = int(io.recvline().decode().strip())
    data = {}
    for name, (func, expr1, expr2) in conf.items():
        data[name] = construct_array(expr1, expr2)

    valid = True
    for var in 'pq':
        mask1 = data[var][2]
        mask2 = data[var][3]
        if sorted([len(mask1), len(mask2)]) != [154, 155]:
            valid = False
            continue
        mask_mul8_1 = data[f'{var}+{var}'][2]
        mask_mul8_2 = data[f'{var}+{var}'][3]
        if sorted([len(mask_mul8_1), len(mask_mul8_2)]) != [154, 155]:
            valid = False
            continue

        if len(mask1) + len(mask_mul8_1) != 154 + 155:
            valid = False
            continue
        p_idx_8 = 0 if len(mask1) == 154 else 1
        leading_digit = data[var][p_idx_8][-2]
        leading_digit_mul8 = data[f'{var}+{var}'][p_idx_8][-1]
        if (leading_digit * 8) // 10 >= leading_digit_mul8:
            valid = False
            continue
        if valid:
            break
    if not valid:
        io.close()
        continue
    count = 0
    # just to check how many pairs (k, n-k) is of same number of digits
    for key in ['p', 'q', 'p+p', 'p+q', 'q+q', 'pxp', 'qxq', 'p-q']:
        if len(data[key][2]) != len(data[key][3]):
            continue
        count += 1

    if count == 0:   # we must need at least 1 pair of k, n-k with both 309 digits to do the next step
        io.close()
        continue

    io.close()
    break
else:
    raise Exception('there is around 1.2% success rate of getting the scenario')

print(f'Done in {i} attempts')
print(f'{c = }')

###############################################################################################################################################################
##### find the smaller one of pow(p, e, n) or pow(-p, e, n) (154 digit), by using the fact pow(p+p, e, n) == pow(p, e, n) * 8
###############################################################################################################################################################

p_idx_8 = 0 if data[var][0][0] is None else 1

data['n'] = []
for i in range(309):
    data['n'].append(set())

for key in ['p', 'q', 'p+p', 'p+q', 'q+q', 'pxp', 'qxq', 'p-q']:
    if len(data[key][2]) != len(data[key][3]):
        continue
    for idx, (v1, v2) in enumerate(zip(data[key][0], data[key][1])):
        if v1 is None or v2 is None:
            continue
        data['n'][idx].add((v1+v2)%10)

p_cands = {}
for idx in range(154):
    cands = []
    for digit in range(10):
        if idx == 0 and (digit + data[var][1-p_idx_8][0]) % 10 not in [1, 3, 7, 9]:
            continue
        test_p = data[var][p_idx_8][:]
        test_p[idx*2] = digit
        sum_p = 0
        #sum_p8 = 0
        for j in range(idx*2+2):
            sum_p += 10**j * test_p[j] * 8
        if ( sum_p % (10 ** (idx*2+1)) ) // (10 ** (idx*2)) != data[f'{var}+{var}'][p_idx_8][idx*2]:
            continue
        n_cands = data['n'][idx*2]
        if len(n_cands) == 2:
            n_vals = n_cands
        else:
            n_val = next(iter(n_cands))
            n_vals = [(n_val-1)%10, n_val, (n_val+1)%10]
        if (digit + data[var][1-p_idx_8][idx*2]) % 10 not in n_vals:
            continue
        cands.append(digit)

    if not cands:
        raise Exception('something wrong')
        raise
    if len(cands) != 1:
        raise Exception('something wrong here')
    data[var][p_idx_8][idx*2] = cands[0]

p_val = sum([digit * 10 ** idx for idx, digit in enumerate(data[var][p_idx_8]) if digit is not None])
print('pow(%s%s, e, n) = %d' % (('-' if p_idx_8 == 1 else ''), var, p_val))


#####################################################################################
### update the values of the found pow(p, e, n) and pow(2p, e, n) into the arrays

val_1 = str(p_val * 8)[::-1]

v1, v2, res1, res2 = data[f'{var}+{var}']
if p_idx_8 == 0:
    data[f'{var}+{var}'] = ([int(i) for i in val_1], v2, res1, res2)
else:
    data[f'{var}+{var}'] = (v1, [int(i) for i in val_1], res1, res2)


### update n, but actually nothing useful, we don't need it, except getting the ending digit of n

for idx, (digit1, digit2) in enumerate(zip(data[f'{var}+{var}'][p_idx_8], data[f'{var}+{var}'][1-p_idx_8])):
    if digit1 is not None and digit2 is not None:
        data['n'][idx].add((digit1+digit2) % 10)

n_cands = []
for idx in range(309):
    digit_sets = data['n'][idx]
    if digit_sets == set([9, 0]):
        n_cands.append([0])
    elif len(digit_sets) == 2:
        n_cands.append([max(digit_sets)])
    else:
        digit = next(iter(digit_sets))
        n_cands.append([digit, (digit+1)%10])

# n must be odd
n_cands[0] = [d for d in n_cands[0] if d % 2 == 1]

# prepare to compute all digits of n

p_val1_1 = [int(digit) for digit in str(p_val)[::-1]] + [0]
p_val1_2 = data[var][1-p_idx_8]

p_val2_1 = [int(digit) for digit in str(p_val*8)[::-1]]
p_val2_2 = data[f'{var}+{var}'][1-p_idx_8]

n_digits = [n_cands[0][0]]
for idx in range(0, 308):
    if idx % 2 == 0:
        add_1 = 0
        for j in range(idx):
            if p_val2_1[j] + p_val2_2[j] + add_1 >= 10:
                add_1 = 1
            else:
                add_1 = 0
        p_val2_2[idx] = (n_digits[idx] - p_val2_1[idx] - add_1) % 10
        for j in range(idx, idx+1):
            if p_val2_1[j] + p_val2_2[j] + add_1 >= 10:
                add_1 = 1
            else:
                add_1 = 0
        new_digit = (p_val2_1[idx+1] + p_val2_2[idx+1] + add_1) % 10
        n_digits.append(new_digit)
    else:
        add_1 = 0
        for j in range(idx):
            if p_val1_1[j] + p_val1_2[j] + add_1 >= 10:
                add_1 = 1
            else:
                add_1 = 0
        p_val1_2[idx] = (n_digits[idx] - p_val1_1[idx] - add_1) % 10
        for j in range(idx, idx+1):
            if p_val1_1[j] + p_val1_2[j] + add_1 >= 10:
                add_1 = 1
            else:
                add_1 = 0

        new_digit = (p_val1_1[idx+1] + p_val1_2[idx+1] + add_1) % 10
        n_digits.append(new_digit)

n = sum_coeff(n_digits)
print(f'{n = }')

p = gcd(p_val, n)
q = n // p
print(f'{p = }')
print(f'{q = }')

d = pow(e, -1, (p-1)*(q-1))
print(long_to_bytes(pow(c, d, n)))
