from pwn import *

class matroid_intersection:
	def __init__(self, n):
		self.n = n
		self.pv = [-1] * self.n
		self.q = [0] * (n + 1)
	def forward_edge(self, u):
		res = []
		self.m1.clear()
		for v in range(self.n):
			if self.state[v] and u != v:
				self.m1.insert(v)
		for v in range(self.n):
			if not self.state[v] and self.pv[v] == -1 and self.m1.check(v):
				res.append(v)
				self.pv[v] = u
		return res
	def backward_edge(self, u):
		self.m2.clear()
		for it in range(2):
			for v in range(self.n):
				if (u == v or self.state[v]) and int(self.pv[v] == -1) == it:
					if not self.m2.check(v):
						if it:
							self.q[self.end], self.end, self.pv[v] = v, self.end + 1, u
							return v
						else:
							return -1
					self.m2.insert(v)
		return self.n
	def augment(self):
		self.pv = [-1] * self.n
		self.q[0] = self.n
		beg, self.end = 0, 1
		while beg < self.end:
			u, beg = self.q[beg], beg + 1
			for w in self.forward_edge(u):
				while (v := self.backward_edge(w)) >= 0:
					if v == self.n:
						while w != self.n:
							self.state[w], w = not self.state[w], self.pv[w]
						return True
		return False
	def maximum_common_independent_set(self, m1, m2):
		self.m1 = m1
		self.m2 = m2
		self.state = [False] * self.n
		self.m1.clear()
		self.m2.clear()
		for u in range(self.n):
			if self.m1.check(u) and self.m2.check(u):
				self.state[u] = True
				self.m1.insert(u)
				self.m2.insert(u)
		while self.augment():
			pass
		return [u for u in range(self.n) if self.state[u]]

class disjoint_set:
	def __init__(self, n):
		self.n = n
		self.p = [-1] * self.n
	def root(self, u):
		if self.p[u] < 0:
			return u
		self.p[u] = self.root(self.p[u])
		return self.p[u]
	def share(self, u, v):
		return self.root(u) == self.root(v)
	def merge(self, u, v):
		u, v = self.root(u), self.root(v)
		if u == v:
			return False
		if self.p[u] > self.p[v]:
			u, v = v, u
		self.p[u] += self.p[v]
		self.p[v] = u
		return True
	def clear(self):
		self.p = [-1] * self.n

class graphic_matroid:
	def __init__(self, V, edges):
		self.V = V
		self.edges = edges
		self.ds = disjoint_set(V)
	def check(self, i):
		return not self.ds.share(self.edges[i][0], self.edges[i][1])
	def insert(self, i):
		assert self.ds.merge(self.edges[i][0], self.edges[i][1])
	def clear(self):
		self.ds.clear()

class F2_linear_matroid:
	def __init__(self, elem):
		self.elem = elem
		self.basis = []
	def reduce(self, x):
		for b in self.basis:
			x = min(x, x ^ b)
		return x
	def check(self, i):
		return self.reduce(self.elem[i]) != 0
	def insert(self, i):
		x = self.reduce(self.elem[i])
		assert x > 0
		for i, b in enumerate(self.basis):
			if x > b:
				self.basis.insert(i, x)
				x = -1
				break
		if x != -1:
			self.basis.append(x)
	def clear(self):
		self.basis = []

def handle_pow(r):
    r.recvuntil(b'python3 ')
    r.recvuntil(b' solve ')
    challenge = r.recvline().decode('ascii').strip()
    log.info(f"POW: {challenge}")
    result = subprocess.run(
        ['bash', '-c', f'python3 <(curl -sSL https://goo.gle/kctf-pow) solve {challenge}'],
        capture_output=True,
        text=True
    )
    solution = result.stdout.strip().encode()
    r.sendline(solution)
    r.recvuntil(b'Correct\n')

# server = process(["python3", "server.py"])
server = remote("game-with-rin.challs.csc.tf", 1337)
server.recvuntil(b'== proof-of-work: ')
if server.recvline().startswith(b'enabled'):
    handle_pow(server)

for _ in range(13):
	print(server.recvline())

for _ in range(200):
	print(server.recvline())
	print(server.recvuntil(b"Server> V = "), end = "")
	V = int(server.recvline().strip().decode())
	print(f"{V}")
	print(server.recvuntil(b"Server> edges = "), end = "")
	edges = eval(server.recvline().strip().decode())
	print(f"{len(edges)}")

	print(server.recvline())
	print(server.recvuntil(b"You> "))
	
	mi = matroid_intersection(len(edges))
	iset = mi.maximum_common_independent_set(graphic_matroid(V, edges), F2_linear_matroid([w for u, v, w in edges]))

	if len(iset) == V - 1:
		print(f"Going first")
		server.sendline(b"first")
		print(server.recvline())
		print(server.recvline())
		print(server.recvuntil(b"S = "))
		S = iset
		server.sendline(" ".join([str(i) for i in S]).encode())
		
		print(f"Chosen {S = }")
		print(server.recvline())
		print(server.recvline())
		print(server.recvline())

	else:
		print(f"Going second")
		server.sendline(b"second")
		print(server.recvline())
		print(server.recvuntil(b"S = "))
		S = list(map(int, server.recvline().strip().decode().split(" ")))
		print(f"{S = }")
		print(server.recvline())
		print(server.recvline())
		print(server.recvuntil(b"T = "))
		rref = []
		for bit in range(V):
			x = 0
			for i in range(len(S)):
				if edges[S[i]][2] >> bit & 1:
					x |= 1 << i
			for b in rref:
				x = min(x, x ^ b)
			if x == 0:
				continue
			for i in range(len(rref)):
				rref[i] = min(rref[i], rref[i] ^ x)
			for i, b in enumerate(rref):
				if b < x:
					rref.insert(i, x)
					x = -1
					break
			if x != -1:
				rref.append(x)
		pivot = 0
		for b in rref:
			pivot |= 1 << b.bit_length() - 1
		for i in range(len(S)):
			if pivot >> i & 1:
				continue
			dep_set = [S[i]] + [S[b.bit_length() - 1] for b in rref if b >> i & 1]
			from random import Random
			Random().shuffle(dep_set)
			server.sendline(" ".join([str(i) for i in dep_set]).encode())
			pivot = -1
			break
		assert pivot == -1
		print(server.recvline())

print(server.recvline())
print(server.recvline())
print(server.recvline())
