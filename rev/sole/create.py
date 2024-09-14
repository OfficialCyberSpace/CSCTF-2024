import random
flag = "CSCTF{ruSt_15_c00l_r1gHt?}"
operations = ["+", "-", "*"]
size = len(flag)

eq = []
unused = list(range(size))

for i in range(30):
    a, b, c = 0, 0, 0
    while a == b or b == c or c == a:
        a, b, c = random.randint(0, size-1), random.randint(0, size-1), random.randint(0, size-1)
    
    l, r = random.choice(operations), random.choice(operations)
    result = eval(f"{ord(flag[a])} {l} {ord(flag[b])} {r} {ord(flag[c])}")
    print(f"if _{a} {l} _{b} {r} _{c} != {result} {{\n\tx = 1;\n}}\n")
    eq.append(f"solver.add(flag[{a}] {l} flag[{b}] {r} flag[{c}] == {result})")

    for idx in [a, b, c]:
        if idx in unused:
            unused.remove(idx)

for e in eq:
    print(e)

print(unused)