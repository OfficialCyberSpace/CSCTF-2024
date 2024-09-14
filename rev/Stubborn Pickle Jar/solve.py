import random

GOAL = b"\x00\x00\x00\x00\x00-\xea\x12Xe\xfeP\xfe\xd7\xf2)&U\x08,#\x82b\xd8\x85b\xe8\xf7_\x1c\xf8P\\2\xec\x9b\x9c\xfai\xc3q\x12\xad#\x8a<\xab\x8e'c\xd5+6\x92\xaee\x18c\xb0\x0e\x87\x06\xab4E\x98\xda\x8a\xd3"

known = b"CSCTF{"
for length in range(42, 69+1):
    print(f"Trying length {length}")

    random.seed(4)
    lst = list(range(0, 73))
    random.shuffle(lst)
    lst = list(reversed(lst))
    [lst.pop(0) for _ in range(73 - length)]
    
    e = list(map(str.count, map(bin, lst), '1'*69))
    f = list(map(int.bit_length, lst))
    g = map(int.__lshift__, e, f)
    h = list(map(int.__rmod__, [256]*69, g))
    ii = map(int.__add__, h, f)
    j = list(map(int.__add__, ii, e))
    x = list(map(int.__xor__, lst, j))

    try:
        flag = bytes([pow(GOAL[~i] ^ d, -1, 257) for i, d in enumerate(x)])
        if known not in flag:
            continue
    except:
        continue

    print(f"Flag for length {length} found!")
    print(flag)
    exit()
print("Failed everything :sob:")