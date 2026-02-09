import numpy as np
import itertools

table = {
    "000": "000000",
    "100": "110100",
    "010": "011010",
    "110": "101110",
    "001": "101001",
    "101": "011101",
    "011": "110011",
    "111": "000111",
}

def bits(s):
    return np.array([int(ch) for ch in s], dtype=int)

c100 = bits(table["100"])
c010 = bits(table["010"])
c001 = bits(table["001"])

G = np.vstack([c100, c010, c001])

def encode(u_bits):
    u = np.array(u_bits, dtype=int)
    return (u @ G) % 2

ok = True
for u_str, c_str in table.items():
    u = bits(u_str)
    c = bits(c_str)
    if not np.array_equal(encode(u), c):
        ok = False
        break

def nullspace_basis_gf2(G):
    sols = []
    for h in itertools.product([0, 1], repeat=G.shape[1]):
        h = np.array(h, dtype=int)
        if np.all((G @ h) % 2 == 0):
            sols.append(h)
    basis = []
    for v in sols[1:]:
        cand = basis + [v]
        if gf2_rank(np.vstack(cand)) > len(basis):
            basis.append(v)
        if len(basis) == G.shape[1] - G.shape[0]:
            break
    return np.vstack(basis)

def gf2_rank(A):
    A = A.copy() % 2
    r, c = 0, 0
    n, m = A.shape
    while r < n and c < m:
        piv = None
        for i in range(r, n):
            if A[i, c] == 1:
                piv = i
                break
        if piv is None:
            c += 1
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(n):
            if i != r and A[i, c] == 1:
                A[i] ^= A[r]
        r += 1
        c += 1
    return r

H = np.array([
    [0,0,1,0,1,1],
    [0,1,0,1,1,0],
    [1,0,0,1,0,1],
], dtype=int)

print("G=\n", G)
print("Проверка таблицы (u*G == КС):", ok)
print("H=\n", H)
print("G*H^T mod2=\n", (G @ H.T) % 2)

