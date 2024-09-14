from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

# PARAMETERS
q       = 3329
k       = 2
sigma   = 2.5
m = n       = 256
h = floor(.25*n/2)


K   = CyclotomicField(n,"z")
OK      = K.OK()
OKq= OK.quotient(q,'y')
z = K.0

with open('output.txt', 'r') as file:
    lines = file.readlines()

# Extract and parse the data
A_output = eval(lines[0].split('=')[1].strip().replace("^","**"))
b_output = eval(lines[1].split('=')[1].strip().replace("^","**"))
H_output = eval(lines[2].split('=')[1].strip().replace("^","**"))
l2_output = eval(lines[3].split('=')[1].strip().replace("^","**"))
enc = bytes.fromhex(lines[4].split('=')[1].strip())



A = matrix(K,k,k,A_output)
b = vector(K,k,b_output)
H = matrix(K,k,k,H_output)
l2 = vector(K,k,l2_output)



def to_Z(A):
    return block_matrix(ZZ,[ [cof.matrix() for cof in row] for row in A.rows()])


Az = to_Z(A)
bz = vector(ZZ,b[0].list() + b[1].list())
Hz = to_Z(H)
l2z = vector(ZZ,l2[0].list() + (l2[1]).list())
In = identity_matrix(n)

L = block_matrix(ZZ,[
[ q*In               , 0*In                        , 0*In[:,-1]  ],
[   Az               , Hz[:,:-h].augment(In[:,-h:]), 0*In[:,-1]  ],
[   matrix(ZZ,1,n,bz),  matrix(ZZ,1,n,l2z)         , matrix([1]) ]
])

Hl = L[n:2*n+1,n:-h]
c = ceil(sqrt((n+m+1)/(2*pi*exp(1))) * sqrt(det(Hl.T*Hl))^ (1/(n+m+1)) * 2^((n+m+1)/2))

LH = L[n:,m:]
LH[:,:k]*=c
red,T = LH.LLL(transformation = 1)

sc = vector(list(Hz[:-h,:-h].solve_left((l2z-(red[0] * -red[0,-1])[:-1] * Hz)[:-h]))+list ((red[0] * -red[0,-1])[-h-1:-1]))
s = vector([K(list(sc[:n//2])),K(list(sc[n//2:]))])
e = (b-s*A).change_ring(OKq)

key = sha256(str(matrix(s)).encode()).digest()[:16]
iv  = sha256(str(matrix(e)).encode()).digest()[:16]

cipher= AES.new(key,AES.MODE_CBC,iv=iv)
print(unpad(cipher.decrypt(enc),16).decode())