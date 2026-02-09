from itertools import product

def xor_vec(x, y):
    return tuple((a ^ b) for a, b in zip(x, y))

def hamming_weight(v):
    return sum(v)

def hamming_distance(x, y):
    return hamming_weight(xor_vec(x, y))

def check_hamming_metric(n: int):
    V = list(product([0, 1], repeat=n))

    for x in V:
        for y in V:
            dxy = hamming_distance(x, y)
            if dxy < 0:
                return False, "non-negativity"
            if (dxy == 0) != (x == y):
                return False, "identity"
            if dxy != hamming_distance(y, x):
                return False, "symmetry"

    for x in V:
        for y in V:
            dxy = hamming_distance(x, y)
            for z in V:
                dxz = hamming_distance(x, z)
                dyz = hamming_distance(y, z)
                if dxz > dxy + dyz:
                    return False, "triangle"

    return True, "ok"

if __name__ == "__main__":
    for n in range(1, 9):
        print(n, check_hamming_metric(n))

