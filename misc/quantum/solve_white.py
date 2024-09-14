from pwn import *
from subprocess import check_output

r=remote("quantum.challs.csc.tf", 1337)
r.recvuntil(b'You can run the solver with:'); r.recvline()
pow_comm = r.recvline().strip().decode().split('solve ')[1]
print(pow_comm)
poww = check_output(['./pow.py', 'solve', pow_comm]).strip()
print(poww)
r.recv()
r.sendline(poww.strip())
print(r.recvline())

n=int(r.recvline().decode())
print(f'{n = }')

r.recvuntil(b'Ask me anything?\n')

points = []
for i in range(1, n, 2):
    points.append((i,1))
    #points.append((i+1,1))
while points[-1][0]>=n:
    points.pop(-1)
if (n-3, 1) not in points:
    points.append((n-3, 1))
if (n-2, 1) not in points:
    points.append((n-2, 1))
if (n-1, 1) not in points:
    points.append((n-1, 1))


xs = " ".join([str(i[0]) for i in points])
ys = " ".join([str(i[1]) for i in points])

r.sendline(str(len(points)).encode())
r.sendline(xs.encode())
r.sendline(ys.encode())

sumsx = [0]*(n-1)

sums = r.recvline(keepends=False).decode()
sums = list(map(int, sums.split()))
for i, p in zip(sums, points):
    sumsx[p[0]-1] = i
orig = sumsx[0]
diffx = [0]*(n-3)

for i in range(len(sumsx)-2):
    if sumsx[i]!=0 and sumsx[i+2] !=0:
        diffx[i] = sumsx[i] - sumsx[i+2]
m = len(points)

print(sumsx, diffx)

for i in range(len(diffx)):
    if diffx[i] == 0 and diffx[i-1] == diffx[i+1]:
        diffx[i] = diffx[i-1]
        sumsx[i] = sumsx[i-1] - diffx[i]//2
        sumsx[i+2] = sumsx[i+1] - diffx[i]//2

points = []
for i in range(1, n):
    if sumsx[i-1] == 0:
        points.append((i,1))
m+=len(points)
xs = " ".join([str(i[0]) for i in points])
ys = " ".join([str(i[1]) for i in points])

r.sendline(str(len(points)).encode())
r.sendline(xs.encode())
r.sendline(ys.encode())

sums = r.recvline(keepends=False).decode()
sums = list(map(int, sums.split()))
for i, p in zip(sums, points):
    sumsx[p[0]-1] = i




points = []
for i in range(3, n, 2):
    points.append((1,i))
    #points.append((i+1,1))
while points[-1][0]>=n:
    points.pop(-1)
if (1, n-3) not in points:
    points.append((1, n-3))
if (1, n-2) not in points:
    points.append((1, n-2))
if (1, n-1) not in points:
    points.append((1, n-1))


xs = " ".join([str(i[0]) for i in points])
ys = " ".join([str(i[1]) for i in points])

r.sendline(str(len(points)).encode())
r.sendline(xs.encode())
r.sendline(ys.encode())

sumsy = [0]*(n-1)

sums = r.recvline(keepends=False).decode()
sums = list(map(int, sums.split()))
for i, p in zip(sums, points):
    sumsy[p[1]-1] = i
sumsy[0] = orig
diffy = [0]*(n-3)

for i in range(len(sumsy)-2):
    if sumsy[i]!=0 and sumsy[i+2] !=0:
        diffy[i] = sumsy[i] - sumsy[i+2]
m += len(points)

for i in range(len(diffy)):
    if diffy[i] == 0 and diffy[i-1] == diffy[i+1]:
        diffy[i] = diffy[i-1]
        sumsy[i] = sumsy[i-1] - diffy[i]//2
        sumsy[i+2] = sumsy[i+1] - diffy[i]//2

points = []
for i in range(1, n):
    if sumsy[i-1] == 0:
        points.append((1,i))
m+=len(points)
xs = " ".join([str(i[0]) for i in points])
ys = " ".join([str(i[1]) for i in points])

r.sendline(str(len(points)).encode())
r.sendline(xs.encode())
r.sendline(ys.encode())

sums = r.recvline(keepends=False).decode()
sums = list(map(int, sums.split()))
for i, p in zip(sums, points):
    sumsy[p[1]-1] = i

print(sumsx, sumsy, m, n*1.9)
r.sendline(b'-1')

diffx = [0]*(n-1)
diffy = [0]*(n-1)

for i in range(n-1):
    diffx[i] = sumsx[0] - sumsx[i]
    diffy[i] = sumsy[0] - sumsy[i]
print(diffx, diffy)

points = {}
for i in range(1, n):
    for j in range(1, n):
        points[(i, j)] = orig - diffx[i-1] - diffy[j-1]
r.recvuntil(b'It is easy to prove that you can answer the following queries!\n')
#print(points)
def query(x0, y0, x1, y1):
    sum = 0
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            sum += points[(x, y)]
    return sum

q = int(r.recvline(keepends=False).decode())
results = [0]*q
for i in range(q):
    x0, y0, x1, y1 = list(map(int, r.recvline(keepends=False).decode().split()))
    results[i] = str(query(x0, y0, x1, y1))
r.sendline(' '.join(results).encode())
print(results)
print(points[(100, 100)])
r.interactive()