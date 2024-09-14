import gdb, string, re

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + "{}_"

flag = ''
gdb.execute("break *0x555555555388") #3bc

def iterate(lastout):
    try:
        out = gdb.execute("x/x $rbp-0x138", to_string=True)
        match = re.split("0x7fffffffdd58:\t", out)
        out = int(match[1], 16)
        #print("gather success", out)
        if(out > lastout):
            gdb.execute("continue")
            #print("continuing")
            lastout = iterate(out)
    except:
        print("End of file")
    return lastout

for i in range(0, 32):
    if(len(flag) != i):
        print("Error")
        quit()
    for c in alphabet:
        padding = "a" * (32-(i+1))
        print(flag + c)
        gdb.execute("r <<<" + flag + c + padding)
        out = iterate(-1)
        print(out)
        if(out > i):
            flag = flag + c
            print(flag)
            break

print(flag)