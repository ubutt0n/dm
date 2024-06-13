from sympy import isprime, factorint
from itertools import *
from math import lcm
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def decompose_ring(mod):
    if not isprime(mod):
        factors = factorint(mod)
        isomorph_rings = [p**e for p, e in factors.items()]
        return isomorph_rings
    else:
        return [mod]

def modular_pow(base, deg, mod):
    c = 1
    for i in range(1, deg+1):
        c = (c * base) % mod
    return c

def gcdx(a, b):
    u, v = 1, 0
    u_, v_ = v, u

    while b != 0:
        k, r = a // b, a % b
        a, b = b, r
        u, u_ = u_, u-k*u_
        v, v_ = v_, v-k*v_
    if a < 0:
        a, u, v = -a, -u, -v
    return a, u, v

def find_idem(mod):
    isomorph = decompose_ring(mod)
    if len(isomorph) == 1: return [0, 1]
    if len(isomorph) == 2:
        idem = gcdx(isomorph[0], isomorph[1])
        return [0, 1, (idem[2]*isomorph[1])%mod, (idem[1]*isomorph[0])%mod]
    
    idem = [0, 1]
    n = len(isomorph) - 1
    sopost = []
    while len(idem) != len(isomorph)**2:
        arr = []
        for i in combinations(isomorph, n):
            res = 1
            for j in i:
                res *= j
            arr.append(res)
        for i in arr:
            idem0 = gcdx(i, mod/i)
            idem.append(int((idem0[1]*i)%mod))
            idem.append(int((idem0[2]*(mod/i))%mod))
            if n == len(isomorph) - 1: sopost.append(int((idem0[1]*i)%mod))
        if n-1 != 1:
            n -= 1
        else: break
    
    return set(idem), sopost[::-1]
    
def eyler(x):
    factors = factorint(x)
    fact = [(i, e) for i, e in factors.items()]
    if fact[0][0] == 2 and fact[0][1] > 2: 
        return round((fact[0][0]**fact[0][1] - fact[0][0]**(fact[0][1] - 1))/2)

    res = fact[0][0]**fact[0][1] - fact[0][0]**(fact[0][1] - 1)
    return res

def primitive_root(max_ord, mod):
    if max_ord == 1: return 1
    factors = [i for i, _ in factorint(max_ord).items()]
    if len(factors) == 1:
        for i in range(2, mod):
            for j in range(1, max_ord+1):
                if modular_pow(i, j, mod) == 1:
                    if j == max_ord: return i
                    else: break
    for i in range(1, mod):
        if gcdx(i, mod)[0] == 1 and modular_pow(i, int(max_ord/2), mod) != 1:
            flag = True
            for j in factors:
                if modular_pow(i, j, mod) == 1:
                    print(i, j, mod)
                    flag = False
            if flag == True:
                return i

def main(mod):
    isomorph = decompose_ring(mod)
    max_ords = [eyler(i) for i in isomorph]
    idemps = find_idem(mod)
    prime_roots = []
    for e, i in enumerate(max_ords):
        prime_roots.append(primitive_root(i, isomorph[e]))
    if len(isomorph) == 1:
        print("Идемпотенты: ", idemps)
        print("Маскимальный порядок: ", lcm(*max_ords))
        print("Элемент с наибольшим порядком: ", (sum(np.array(prime_roots) * np.array(idemps)))%mod)
        return [idemps, lcm(*max_ords), (sum(np.array(prime_roots) * np.array(idemps)))%mod]
    if len(isomorph) == 2:
        print("Идемпотенты: ", idemps)
        print("Маскимальный порядок: ", lcm(*max_ords))
        print("Элемент с наибольшим порядком: ", (sum(np.array(prime_roots) * np.array(idemps[2::])))%mod)
        return [idemps, lcm(*max_ords), (sum(np.array(prime_roots) * np.array(idemps[2::])))%mod]
    
    print("Идемпотенты: ", idemps[0])
    print("Маскимальный порядок: ", lcm(*max_ords))
    print("Элемент с наибольшим порядком: ", (sum(np.array(prime_roots) * np.array(idemps[1])))%mod)

    return [idemps[0], lcm(*max_ords), (sum(np.array(prime_roots) * np.array(idemps[1])))%mod, idemps[1]]



mod = int(input("Модуль: "))
results = main(mod)

print("\n\n-------------Тесты-------------")
print("Количество идемпотентов равно 2 в степени количество изоморфных колец?")
print(len(results[0]) == 2**len(decompose_ring(mod)))
print("Все найденные идемпотенты являются идемпотентами?")
flag = True
for i in results[0]:
    if (i**2)%mod != i:
        #print(i, "Не является идемпотентом")
        flag = False
        break
print(flag)
if flag == False:
    print("Все найденные идемпотенты для сопоставления являются идемпотентами?")
    flag == True
    for i in results[3]:
        if (i**2)%mod != 1:
            flag = False
            break
    print(flag)
if mod < 10**4:
    print("Порядок найденного элемента с наибольшим порядком совпадает с наибольшим порядком?")
    for i in range(1, results[1] + 1):
        if modular_pow(results[2], i, mod) == 1:
            if i == results[1]: print(True)
            else:
                print(False)
                break