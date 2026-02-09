import numpy as np
from math import comb

# таблица (для проверки)
code = {
    "00": np.array([0,0,0,0,0], dtype=int),
    "01": np.array([1,0,1,1,0], dtype=int),
    "10": np.array([0,1,0,1,1], dtype=int),
    "11": np.array([1,1,1,0,1], dtype=int),
}

def hamming(a, b):
    return int(np.sum(a != b))

# dmin
words = list(code.values())
dmin = min(hamming(words[i], words[j]) for i in range(len(words)) for j in range(i+1, len(words)))
t = (dmin - 1) // 2

# вероятность ошибки для BSC при t=1 (ошибка, если >=2 битовых ошибок в блоке)
p = 1e-3
Pe = sum(comb(5, i) * (p**i) * ((1-p)**(5-i)) for i in range(t+1+1, 6))  # i=2..5

# порождающая матрица (строки = КС для ИС 10 и 01)
G = np.array([
    [0,1,0,1,1],  # 10 -> 01011
    [1,0,1,1,0],  # 01 -> 10110
], dtype=int)

# проверочная матрица (один из вариантов)
H = np.array([
    [0,0,1,1,1],
    [0,1,0,0,1],
    [1,0,0,1,1],
], dtype=int)

print("dmin =", dmin, " t =", t)
print("Pe =", Pe)

print("\nG=\n", G)
print("\nH=\n", H)

# проверка ортогональности: G * H^T = 0 (mod 2)
check = (G @ H.T) % 2
print("\nG*H^T mod2 =\n", check)

