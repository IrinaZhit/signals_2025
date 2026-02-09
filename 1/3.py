from itertools import product, combinations

def xor_vec(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def wt(v):
    return sum(v)

def hamming(a, b):
    return wt(xor_vec(a, b))

def dmin(codewords):
    cw = list(codewords)
    d = None
    for i in range(len(cw)):
        for j in range(i + 1, len(cw)):
            dij = hamming(cw[i], cw[j])
            d = dij if d is None else min(d, dij)
    return d if d is not None else 0

def all_error_patterns(n, max_wt):
    e0 = (0,) * n
    yield e0
    for w in range(1, max_wt + 1):
        for pos in combinations(range(n), w):
            e = [0] * n
            for i in pos:
                e[i] = 1
            yield tuple(e)

def nn_decode(r, codewords):
    best = None
    best_d = None
    for c in codewords:
        d = hamming(r, c)
        if best_d is None or d < best_d:
            best_d = d
            best = c
        elif d == best_d:
            best = None  # неоднозначно (ничья)
    return best, best_d

def verify_theorem(codewords):
    codewords = list(codewords)
    n = len(codewords[0])
    d = dmin(codewords)
    t = (d - 1) // 2

    for c in codewords:
        for e in all_error_patterns(n, t):
            r = xor_vec(c, e)
            dec, _ = nn_decode(r, codewords)
            if dec != c:
                return False, {"dmin": d, "t": t, "c": c, "e": e, "r": r, "decoded": dec}
    return True, {"dmin": d, "t": t}

if __name__ == "__main__":
    # пример: (5,2)-код из ДЗ1
    code = {
        "00": (0,0,0,0,0),
        "01": (1,0,1,1,0),
        "10": (0,1,0,1,1),
        "11": (1,1,1,0,1),
    }
    ok, info = verify_theorem(code.values())
    print(ok, info)

