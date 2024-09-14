flag = "CSCTF{I_just_wanted_to_spend_time_with_you_baka!}"

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

class NanakuraRin:
	def __init__(self, V, edges):
		self.V = V
		self.edges = [e for e in edges]
	def first_move(self):
		from random import Random
		mi = matroid_intersection(len(self.edges))
		iset = mi.maximum_common_independent_set(graphic_matroid(self.V, self.edges), F2_linear_matroid([w for u, v, w in self.edges]))
		if len(iset) == self.V - 1:
			Random().shuffle(iset)
			return iset
		ds = disjoint_set(self.V)
		for i in iset:
			assert ds.merge(self.edges[i][0], self.edges[i][1])
		for i, (u, v, w) in enumerate(self.edges):
			if ds.merge(u, v):
				iset.append(i)
		Random().shuffle(iset)
		return iset
	def read_first_move(self, S):
		assert len(S) == self.V - 1
		self.S = S
	def second_move(self):
		rref = []
		for bit in range(self.V):
			x = 0
			for i in range(len(self.S)):
				if self.edges[self.S[i]][2] >> bit & 1:
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
		from random import Random
		r = Random()
		for i in range(len(self.S)):
			if pivot >> i & 1:
				continue
			ret = [self.S[i]] + [self.S[b.bit_length() - 1] for b in rref if b >> i & 1]
			r.shuffle(ret)
			return ret
		ret = Random().sample(self.S, r.randrange(1, len(self.S) + 1))
		r.shuffle(ret)
		return ret


def generate_independent_set(X):
	from random import Random
	r = Random()
	s, basis = [], []
	while len(s) < X:
		vec = r.randrange(1, 2**X)
		reduced = vec
		for b in basis:
			reduced = min(reduced, reduced ^ b)
		if reduced == 0:
			continue
		s.append(vec)
		for i, b in enumerate(basis):
			if reduced > b:
				basis.insert(i, reduced)
				reduced = -1
				break
		if reduced != -1:
			basis.append(reduced)
	return s

def generate_tree(V):
	from random import Random
	r = Random()
	edges = []
	for u in range(1, V):
		v = r.randrange(0, u)
		if r.randrange(0, 2) > 0:
			u, v = v, u
		edges.append((u, v))
	r.shuffle(edges)
	return [e for e in edges]

def generate_simply_connected_graph(V, E):
	from random import Random
	r = Random()
	assert V - 1 <= E <= V * (V - 1) // 2
	edges = generate_tree(V)
	found = set()
	for u, v in edges:
		found.add((u, v))
		found.add((v, u))
	while len(edges) < E:
		u, v = r.randrange(0, V), r.randrange(0, V)
		if u == v or (u, v) in found:
			continue
		edges.append((u, v))
		found.add((u, v))
		found.add((v, u))
	return [e for e in edges]

def generate_graph(round_number):
	from random import Random
	r = Random()
	V = max(30, round_number)
	coef = 1.5
	if r.randrange(0, 3) == 0:
		VL = r.randrange(5, V - 20)
		VR = V + 1 - VL
		EL = r.randrange(VL, int(coef * VL) + 1)
		ER = r.randrange(VR, int(coef * VR) + 1)
		edgesL = [(u, v, w) for (u, v), w in zip(generate_simply_connected_graph(VL, EL), generate_independent_set(VL - 1))]
		edgesR = [(VL - 1 + u, VL - 1 + v, w << VL - 1 | r.randrange(0, 2**(VL - 1))) for (u, v), w in zip(generate_tree(VR), generate_independent_set(VR - 1))]
		found = set()
		edges = edgesL + edgesR
		for u, v, w in edges:
			found.add((u, v))
			found.add((v, u))
		while len(edgesR) < ER:
			u, v = r.randrange(VL - 1, V), r.randrange(VL - 1, V)
			if u == v or (u, v) in found:
				continue
			edgesR.append((u, v, r.randrange(0, 2**(VL - 1))))
			found.add((u, v))
			found.add((v, u))
		edges = edgesL + edgesR
	elif r.randrange(0, 10) == 0:
		VL = r.randrange(10, V - 10)
		VR = V + 1 - VL
		EL = r.randrange(VL, int(coef * VL) + 1)
		ER = r.randrange(VR, int(coef * VR) + 1)
		edgesL = [(u, v, r.randrange(1, 2**(VL - 2))) for u, v in generate_simply_connected_graph(VL, EL)]
		edgesR = [(VL - 1 + u, VL - 1 + v, r.randrange(1, 2**(VR - 1))) for u, v in generate_simply_connected_graph(VR, ER)]
		edges = edgesL + edgesR
	else:
		E = r.randrange(V, int(coef * V) + 1)
		edges = [(u, v, r.randrange(1, 2**(V - 1))) for u, v in generate_simply_connected_graph(V, E)]
		if r.randrange(0, 6) == 0:
			convert = [r.randrange(1, 2**(V - 1)) for _ in range(V - 1)]
			for i in range(len(edges)):
				w = edges[i][2]
				w_next = 0
				for bit in range(V - 1):
					if w >> bit & 1:
						w_next ^= convert[bit]
				edges[i] = (edges[i][0], edges[i][1], w_next);
	r.shuffle(edges)
	label = [u for u in range(V)]
	r.shuffle(label)
	convert = generate_independent_set(V - 1)
	for i in range(len(edges)):
		w = edges[i][2]
		w_next = 0
		for bit in range(V - 1):
			if w >> bit & 1:
				w_next ^= convert[bit]
		edges[i] = (edges[i][0], edges[i][1], w_next);
	return V, [(label[u], label[v], w) for u, v, w in edges]