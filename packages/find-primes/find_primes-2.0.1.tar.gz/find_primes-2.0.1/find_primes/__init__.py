'''
A module to finds all kinds of primes.
Python version: 3.6+ (If runs test)
'''

from time import time
from math import log, factorial, sqrt, log2, ceil, floor, gcd
from random import randint, getrandbits
from sys import version_info

NUMPY_ENABLED = True
try:
    from numpy import ones, nonzero, __version__
    print('Detected numpy version {__version__}'.format(**locals()))

except ImportError:
    NUMPY_ENABLED = False

print()

PRIME_TEST = True
FACTOR_TEST = True

LEFT = 'left'
RIGHT = 'right'
BOTH = 'both'
TRIANGLE = 'triangle'
SQUARE = 'square'
PENTAGON = 'pentagon'
HEXAGON = 'hexagon'
HEPTAGON = 'heptagon'

def _check_num(n):
    '''
    Internel function to check the input.
    '''
    if not isinstance(n, int):
        raise TypeError('Type of argument n should be int, got {type(n).__name__}'.format(**locals()))

    if n <= 0:
        raise ValueError('The number of argument n should be greater than 0, got {n}'.format(**locals()))

def is_prime(n):
    '''
    If n is prime, return True.
    '''
    _check_num(n)
    if n in [2, 3, 5, 7]:
        return True

    if not (n % 10 % 2) or n % 10 not in [1, 3, 7, 9] or n == 1 or not isinstance(n, int):
        return False

    for i in range(2, int(n ** 0.5 + 1)):
        if n % i == 0:
            return False

    return True

def all_primes(n, output = 'array'):
    '''
    Return a prime list below n.

    Arguments:
    output ----- 'array' or 'list' ----- The output type of the function.
    '''
    _check_num(n)
    if NUMPY_ENABLED:
        sieve = ones(n + 1, dtype = bool)

    else:
        sieve = [True] * (n + 1)

    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i ** 2, n + 1, i):
                sieve[j] = False

    if NUMPY_ENABLED:
        s = nonzero(sieve)[0]
        if output == 'list':
            return s.tolist()[2:]

        return s[2:]

    else:
        return [x for x in range(2, n + 1) if sieve[x]]

def gen_keys(bits):
    pass

def find_twins(n):
    '''
    Return a dict that has all twin primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    twin_primes = {}
    for ix, xp in enumerate(primes):
        if ix == len(primes) - 1:
            break

        if primes[ix + 1] - xp == 2:
            twin_primes[xp] = primes[ix + 1]

    return twin_primes

def find_palindromes(n):
    '''
    Return a list that has all palindromes primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    palin_primes = []
    for ix, xp in enumerate(primes):
        palin_num = int(str(xp)[::-1])
        if is_prime(palin_num) and palin_num == xp and xp > 10:
            palin_primes.append(palin_num)

    return palin_primes

def find_palindromes_base_2(n):
    '''
    Return a list that has all palindromes primes which was in base 2 below n. (Written in base 10)
    '''
    _check_num(n)
    primes = [bin(x)[2:] for x in all_primes(n)]
    base2_palin_primes = []
    for ix, xp in enumerate(primes):
        palin_num = xp[::-1]
        result = eval(f'0b{palin_num}')
        if is_prime(result) and palin_num == xp:
            base2_palin_primes.append(result)

    return base2_palin_primes

def find_reverses(n):
    '''
    Return a dict that has all reverse primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    reverse_primes = {}
    for ix, xp in enumerate(primes):
        reverse_num = int(str(xp)[::-1])
        if is_prime(reverse_num) and xp > 10:
            reverse_primes[xp] = reverse_num

    palin_primes = find_palindromes(n)
    for x in palin_primes:
        if reverse_primes.get(x):
            reverse_primes.pop(x)

    return reverse_primes

def find_square_palindromes(n):
    '''
    Return a dict that has all square palindrome primes below n.
    '''
    _check_num(n)
    palin_primes = find_palindromes(n)
    square_palin_prime = {}
    for x in palin_primes:
        if str(x ** 2)[::-1] == str(x ** 2):
            square_palin_prime[x] = x ** 2

    return square_palin_prime

def find_arithmetic_prime_progressions(n):
    '''
    Return a list that has all arithmetic prime progression below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    time = 0
    arithmetic_prime_list = []
    for i, xp in enumerate(primes):
        for j in range(i + 1, len(primes)):
            a0, a1 = primes[i], primes[j]
            an = a1 + a1 - a0
            k = []
            while an < n and an in primes:
                k.append(an)
                an += a1 - a0

            if len([a0, a1] + k) >= 3:
                if k and not time:
                    arithmetic_prime_list = [[a0, a1] + k]

                if time:
                    arithmetic_prime_list += [[a0, a1] + k]
                    
                time += 1

    return arithmetic_prime_list

def find_mersennes(n):
    '''
    Return a list that has all mersenne primes below n.
    '''
    _check_num(n)
    primes = set(all_primes(n))
    result = []
    for i in range(2, int(log(n + 1, 2)) + 1):
        result.append(2 ** i - 1)

    mersenne_primes = primes.intersection(result)
    return sorted(mersenne_primes)

def find_double_mersennes(n):
    '''
    Return a list that has all double mersenne primes below n.
    '''
    _check_num(n)
    primes = set(find_mersennes(n))
    result = []
    for i in range(2, int(log(n + 1, 2)) + 1):
        for x in primes:
            result.append(2 ** x - 1)

    mersenne_primes = primes.intersection(result)
    return sorted(mersenne_primes)

def find_fermat_pseudoprimes(n):
    '''
    Return a list that has all fermat pseudoprimes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    a = 2
    fermat_pseudoprimes = []
    composites = [x for x in range(3, n + 1, a) if x not in primes]
    for x in composites:
        if (a ** (x - 1) - 1) % x == 0:
            fermat_pseudoprimes.append(x)

    return fermat_pseudoprimes

def find_balances(n):
    '''
    Return a list that has all balence primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    balence_primes = []
    for ix, xp in enumerate(primes):
        if ix == 0 or ix == len(primes) - 1:
            continue

        if (primes[ix - 1] + primes[ix + 1]) / 2 == xp:
            balence_primes.append(xp)

    return balence_primes

def find_carols(n):
    '''
    Return a list that has all carol primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    carol_primes = [x for x in [(2 ** (x + 1) - 1) ** 2 - 2 for x in range(round(n ** 0.5))] if x in primes]
    return carol_primes

def find_fibonaccis(n):
    '''
    Return a list that has all fibonacci primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    fibs = []
    a = 0
    b = 1
    while a <= n:
        fibs.append(a)
        a, b = b, a + b

    fibonacci_primes = [x for x in primes if x in fibs]
    return fibonacci_primes

def find_truncates(n, direction):
    '''
    Return a list that has all truncatable primes below n.
    Arguments:
    direction ----- The direction to truncate. Choises: LEFT, RIGHT, BOTH
    '''
    _check_num(n)
    primes = all_primes(n)
    truncates = [2, 3, 5, 7]
    if direction == 'left':
        n = False
        for x in primes:
            if x in [2, 3, 5, 7]:
                continue

            prime = [str(x) for x in primes]
            back = x
            x = str(x)
            while True:
                y = x[1:]
                
                if not ((x in prime) and (y in prime)):
                    n = False
                    break
                
                if len(y) <= 1:
                    if (x in prime) and (y in prime):
                        n = True
                        break
                
                x = y

            if n:
                truncates.append(back)

    elif direction == 'right':
        n = False
        for x in primes:
            if x in [2, 3, 5, 7]:
                continue

            prime = [str(x) for x in primes]
            back = x
            x = str(x)
            while True:
                y = x[0:-1]
                
                if not ((x in prime) and (y in prime)):
                    n = False
                    break
                
                if len(y) <= 1:
                    if (x in prime) and (y in prime):
                        n = True
                        break
                
                x = y

            if n:
                truncates.append(back)

    elif direction == 'both':
        out_set = set(truncates)
        result = set(find_truncates(n, 'left')) & set(find_truncates(n, 'right'))
        out_set |= result
        truncates = list(sorted(out_set))

    return truncates

def find_cubans(n):
    '''
    Return a list that has all cuban primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    cuban_primes = []
    for x in range(1, n, 2):
        result = 3 * (x ** 2) + 6 * x + 4
        if result in primes:
            cuban_primes.append(int(result))

    return cuban_primes

def find_center_polygons(n, type):
    '''
    Return a list that has all center polygonal primes below n.
    Arguments:
    type ----- The type of the polygon. Choises: TRIANGLE, SQUARE, PENTAGON, HEXAGON, HEPTAGON
    '''
    _check_num(n)
    primes = all_primes(n)
    center_polygon_primes = []
    if type == 'triangle':
        for i in range(1, n):
            result = (3 * (i ** 2) + 3 * i + 2) / 2
            if result in primes:
                center_polygon_primes.append(int(result))
    
    elif type == 'square':
        for i in range(1, n):
            result = (i ** 2) + (i - 1) ** 2
            if result in primes:
                center_polygon_primes.append(int(result))

    elif type == 'pentagon':
        for i in range(1, n):
            result = (5 * ((i - 1) ** 2) + 5 * (i - 1) + 2) / 2
            if result in primes:
                center_polygon_primes.append(int(result))
    
    elif type == 'hexagon':
        for i in range(1, n):
            result = 1 + 3 * i * (i - 1)
            if result in primes:
                center_polygon_primes.append(int(result))
    
    elif type == 'heptagon':
        for i in range(1, n):
            result = (7 * ((i - 1) ** 2) + 7 * (i - 1) + 2) / 2
            if result in primes:
                center_polygon_primes.append(int(result))

    return center_polygon_primes

def find_wieferiches(n):
    '''
    Return a list that has all wieferich primes below n.
    '''
    _check_num(n)
    primes = all_primes(n, 'list')
    wieferich_primes = []
    for x in primes:
        result = pow(2, x - 1, x ** 2)
        if result == 1:
            wieferich_primes.append(x)

    return wieferich_primes

def find_wilsons(n):
    '''
    Return a list that has all wilson primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    wilson_primes = []
    for x in primes:
        result = (factorial(x - 1) + 1) % (x ** 2)
        if not result:
            wilson_primes.append(x)

    return wilson_primes

def find_happys(n):
    '''
    Return a list that has all happy primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    happy_primes = []
    for x in primes:
        a = []
        num = x
        while num not in a:
            a.append(num)
            num = sum([int(x) ** 2 for x in str(num)])
            if num == 1:
                happy_primes.append(x)
                break
        
    return happy_primes

def find_pierponts(n):
    '''
    Return a list that has all pierpont primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    arr = [False] * (n + 1)
    two = 1
    three = 1
    while two + 1 < n:
        arr[two] = True
        while two * three + 1 < n:
            arr[three] = True
            arr[two * three] = True
            three *= 3
         
        three = 1
        two *= 2
    
    pierpont_primes = []
    for i in range(n):
        if arr[i] and i + 1 in primes:
            pierpont_primes.append(i + 1)
    
    return pierpont_primes

def find_leylands(n):
    '''
    Return a list that has all leyland primes below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    leylands = []
    all_x = []
    for x in range(2, round(n ** 0.5)):
        all_x.append(x)
        for y in range(2, round(n ** 0.5)):
            if not y in all_x:
                ans = x ** y + y ** x
                #ans = fast_pow(x, y) + fast_pow(y, x)
                if ans < n and ans in primes:
                    leylands.append(ans)

    return leylands

def find_leylands_second_kind(n):
    '''
    Return a list that has all leyland primes of the second kind below n.
    '''
    _check_num(n)
    primes = all_primes(n)
    leylands_second_kind = []
    all_x = []
    for x in range(2, round(n ** 0.5)):
        all_x.append(x)
        for y in range(2, round(n ** 0.5)):
            if not y in all_x:
                ans = x ** y - y ** x
                #ans = fast_pow(x, y) - fast_pow(y, x)
                if ans < n and ans in primes:
                    leylands_second_kind.append(ans)

    return list(sorted(leylands_second_kind))

def factor_siqs(n):
    '''
    Return a list that has all factors of n.
    '''
    MAX_DIGITS_POLLARD = 30
    POLLARD_QUICK_ITERATIONS = 20
    MIN_DIGITS_POLLARD_QUICK2 = 45
    POLLARD_QUICK2_ITERATIONS = 25
    SIQS_TRIAL_DIVISION_EPS = 25
    SIQS_MIN_PRIME_POLYNOMIAL = 400
    SIQS_MAX_PRIME_POLYNOMIAL = 4000

    class Polynomial:
        def __init__(self, coeff = [], a = None, b = None):
            self.coeff = coeff
            self.a = a
            self.b = b

        def eval(self, x):
            res = 0
            for a in self.coeff[::-1]:
                res *= x
                res += a
            return res


    class FactorBasePrime:
        def __init__(self, p, tmem, lp):
            self.p = p
            self.soln1 = None
            self.soln2 = None
            self.tmem = tmem
            self.lp = lp
            self.ainv = None

    def lowest_set_bit(a):
        b = (a & -a)
        low_bit = -1
        while (b):
            b >>= 1
            low_bit += 1

        return low_bit

    def to_bits(k):
        k_binary = bin(k)[2:]
        return (bit == '1' for bit in k_binary[::-1])

    def pow_mod(a, k, m):
        r = 1
        b = a
        for bit in to_bits(k):
            if bit:
                r = (r * b) % m

            b = (b * b) % m

        return r

    def is_quadratic_residue(a, p):
        return legendre(a, (p - 1) // 2, 1, p) == 1

    def legendre(a, q, l, n):
        x = q ** l
        if x == 0:
            return 1

        z = 1
        a %= n
        while x != 0:
            if x % 2 == 0:
                a = (a ** 2) % n
                x //= 2

            else:
                x -= 1
                z = (z * a) % n

        return z


    def sqrt_mod_prime(a, p):
        if a == 0:
            return 0

        if p == 2:
            return a

        if p % 2 == 0:
            return None

        p_mod_8 = p % 8
        if p_mod_8 == 1:
            q = p // 8
            e = 3
            while q % 2 == 0:
                q //= 2
                e += 1

            while True:
                x = randint(2, p - 1)
                z = pow_mod(x, q, p)
                if pow_mod(z, 2 ** (e - 1), p) != 1:
                    break

            y = z
            r = e
            x = pow_mod(a, (q - 1) // 2, p)
            v = (a * x) % p
            w = (v * x) % p
            while True:
                if w == 1:
                    return v

                k = 1
                while pow_mod(w, 2 ** k, p) != 1:
                    k += 1

                d = pow_mod(y, 2 ** (r - k - 1), p)
                y = (d ** 2) % p
                r = k
                v = (d * v) % p
                w = (w * y) % p

        elif p_mod_8 == 5:
            v = pow_mod(2 * a, (p - 5) // 8, p)
            i = (2 * a * v * v) % p
            return (a * v * (i - 1)) % p

        else:
            return pow_mod(a, (p + 1) // 4, p)


    def inv_mod(a, m):
        return eea(a, m)[0] % m


    def eea(a, b):
        if a == 0:
            return (0, 1, b)
        x = eea(b % a, a)
        return (x[1] - b // a * x[0], x[0], x[2])

    def is_prime(n):
        if n in [2, 3, 5, 7]:
            return True

        if not (n % 10 % 2) or n % 10 not in [1, 3, 7, 9] or n == 1 or not isinstance(n, int):
            return False

        for i in range(2, int(n ** 0.5 + 1)):
            if n % i == 0:
                return False

        return True

    def siqs_factor_base_primes(n, nf):
        global small_primes
        factor_base = []
        for p in small_primes:
            if is_quadratic_residue(n, p):
                t = sqrt_mod_prime(n % p, p)
                lp = round(log2(p))
                factor_base.append(FactorBasePrime(p, t, lp))
                if len(factor_base) >= nf:
                    break

        return factor_base


    def siqs_find_first_poly(n, m, factor_base):
        p_min_i = None
        p_max_i = None
        for i, fb in enumerate(factor_base):
            if p_min_i is None and fb.p >= SIQS_MIN_PRIME_POLYNOMIAL:
                p_min_i = i
            if p_max_i is None and fb.p > SIQS_MAX_PRIME_POLYNOMIAL:
                p_max_i = i - 1
                break

        if p_max_i is None:
            p_max_i = len(factor_base) - 1

        if p_min_i is None or p_max_i - p_min_i < 20:
            p_min_i = min(p_min_i, 5)

        target = sqrt(2 * float(n)) / m
        target1 = target / ((factor_base[p_min_i].p + factor_base[p_max_i].p) / 2) ** 0.5
        best_q, best_a, best_ratio = None, None, None
        for _ in range(30): 
            a = 1
            q = []
            while a < target1:
                p_i = 0
                while p_i == 0 or p_i in q:
                    p_i = randint(p_min_i, p_max_i)

                p = factor_base[p_i].p
                a *= p
                q.append(p_i)

            ratio = a / target
            if (best_ratio is None or (ratio >= 0.9 and ratio < best_ratio) or best_ratio < 0.9 and ratio > best_ratio):
                best_q = q
                best_a = a
                best_ratio = ratio

        a = best_a
        q = best_q
        s = len(q)
        B = []
        for l in range(s):
            fb_l = factor_base[q[l]]
            q_l = fb_l.p
            gamma = (fb_l.tmem * inv_mod(a // q_l, q_l)) % q_l
            if gamma > q_l // 2:
                gamma = q_l - gamma

            B.append(a // q_l * gamma)

        b = sum(B) % a
        b_orig = b
        if (2 * b > a):
            b = a - b

        g = Polynomial([b * b - n, 2 * a * b, a * a], a, b_orig)
        h = Polynomial([b, a])
        for fb in factor_base:
            if a % fb.p != 0:
                fb.ainv = inv_mod(a, fb.p)
                fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
                fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

        return g, h, B

    def siqs_find_next_poly(n, factor_base, i, g, B):
        v = lowest_set_bit(i) + 1
        z = -1 if ceil(i / (2 ** v)) % 2 == 1 else 1
        b = (g.b + 2 * z * B[v - 1]) % g.a
        a = g.a
        b_orig = b
        if (2 * b > a):
            b = a - b

        g = Polynomial([b * b - n, 2 * a * b, a * a], a, b_orig)
        h = Polynomial([b, a])
        for fb in factor_base:
            if a % fb.p != 0:
                fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
                fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

        return g, h

    def siqs_sieve(factor_base, m):
        sieve_array = [0] * (2 * m + 1)
        for fb in factor_base:
            if fb.soln1 is None:
                continue

            p = fb.p
            i_start_1 = -((m + fb.soln1) // p)
            a_start_1 = fb.soln1 + i_start_1 * p
            lp = fb.lp
            if p > 20:
                for a in range(a_start_1 + m, 2 * m + 1, p):
                    sieve_array[a] += lp

                i_start_2 = -((m + fb.soln2) // p)
                a_start_2 = fb.soln2 + i_start_2 * p
                for a in range(a_start_2 + m, 2 * m + 1, p):
                    sieve_array[a] += lp

        return sieve_array

    def siqs_trial_divide(a, factor_base):
        divisors_idx = []
        for i, fb in enumerate(factor_base):
            if a % fb.p == 0:
                exp = 0
                while a % fb.p == 0:
                    a //= fb.p
                    exp += 1


                divisors_idx.append((i, exp))
            if a == 1:
                return divisors_idx

        return None

    def siqs_trial_division(n, sieve_array, factor_base, smooth_relations, g, h, m, req_relations):
        sqrt_n = sqrt(float(n))
        limit = log2(m * sqrt_n) - SIQS_TRIAL_DIVISION_EPS
        for (i, sa) in enumerate(sieve_array):
            if sa >= limit:
                x = i - m
                gx = g.eval(x)
                divisors_idx = siqs_trial_divide(gx, factor_base)
                if divisors_idx is not None:
                    u = h.eval(x)
                    v = gx
                    smooth_relations.append((u, v, divisors_idx))
                    if (len(smooth_relations) >= req_relations):
                        return True

        return False

    def siqs_build_matrix(factor_base, smooth_relations):
        fb = len(factor_base)
        M = []
        for sr in smooth_relations:
            mi = [0] * fb
            for j, exp in sr[2]:
                mi[j] = exp % 2

            M.append(mi)

        return M

    def siqs_build_matrix_opt(M):
        m = len(M[0])
        cols_binary = [''] * m
        for mi in M:
            for j, mij in enumerate(mi):
                cols_binary[j] += '1' if mij else '0'

        return [int(cols_bin[::-1], 2) for cols_bin in cols_binary], len(M), m

    def add_column_opt(M_opt, tgt, src):
        M_opt[tgt] ^= M_opt[src]

    def find_pivot_column_opt(M_opt, j):
        if M_opt[j] == 0:
            return None

        return lowest_set_bit(M_opt[j])

    def siqs_solve_matrix_opt(M_opt, n, m):
        row_is_marked = [False] * n
        pivots = [-1] * m
        for j in range(m):
            i = find_pivot_column_opt(M_opt, j)
            if i is not None:
                pivots[j] = i
                row_is_marked[i] = True
                for k in range(m):
                    if k != j and (M_opt[k] >> i) & 1:
                        add_column_opt(M_opt, k, j)

        perf_squares = []
        for i in range(n):
            if not row_is_marked[i]:
                perfect_sq_indices = [i]
                for j in range(m):
                    if (M_opt[j] >> i) & 1:
                        perfect_sq_indices.append(pivots[j])

                perf_squares.append(perfect_sq_indices)

        return perf_squares

    def siqs_calc_sqrts(square_indices, smooth_relations):
        res = [1, 1]
        for idx in square_indices:
            res[0] *= smooth_relations[idx][0]
            res[1] *= smooth_relations[idx][1]

        res[1] = sqrt_int(res[1])
        return res

    def sqrt_int(n):
        a = n
        s = 0
        o = 1 << (floor(log2(n)) & ~1)
        while o != 0:
            t = s + o
            if a >= t:
                a -= t
                s = (s >> 1) + o

            else:
                s >>= 1

            o >>= 2

        return s

    def kth_root_int(n, k):
        u = n
        s = n + 1
        while u < s:
            s = u
            t = (k - 1) * s + n // pow(s, k - 1)
            u = t // k
        return s

    def siqs_factor_from_square(n, square_indices, smooth_relations):
        sqrt1, sqrt2 = siqs_calc_sqrts(square_indices, smooth_relations)
        return gcd(abs(sqrt1 - sqrt2), n)


    def siqs_find_factors(n, perfect_squares, smooth_relations):
        factors = []
        rem = n
        non_prime_factors = set()
        prime_factors = set()
        for square_indices in perfect_squares:
            fact = siqs_factor_from_square(n, square_indices, smooth_relations)
            if fact != 1 and fact != rem:
                if is_prime(fact):
                    if fact not in prime_factors:
                        prime_factors.add(fact)

                    while rem % fact == 0:
                        factors.append(fact)
                        rem //= fact

                    if rem == 1:

                        break
                    if is_prime(rem):
                        factors.append(rem)
                        rem = 1
                        break

                else:
                    if fact not in non_prime_factors:
                        non_prime_factors.add(fact)

        if rem != 1 and non_prime_factors:
            non_prime_factors.add(rem)
            for fact in sorted(siqs_find_more_factors_gcd(non_prime_factors)):
                while fact != 1 and rem % fact == 0:
                    factors.append(fact)
                    rem //= fact

                if rem == 1 or is_prime(rem):
                    break

        if rem != 1:
            factors.append(rem)

        return factors

    def siqs_find_more_factors_gcd(numbers):
        res = set()
        for n in numbers:
            res.add(n)
            for m in numbers:
                if n != m:
                    fact = gcd(n, m)
                    if fact != 1 and fact != n and fact != m:
                        if fact not in res:
                            res.add(fact)

                        res.add(n // fact)
                        res.add(m // fact)
        return res

    def siqs_choose_nf_m(d):
        if d <= 34:
            return 200, 65536

        if d <= 36:
            return 300, 65536

        if d <= 38:
            return 400, 65536

        if d <= 40:
            return 500, 65536

        if d <= 42:
            return 600, 65536

        if d <= 44:
            return 700, 65536

        if d <= 48:
            return 1000, 65536

        if d <= 52:
            return 1200, 65536

        if d <= 56:
            return 2000, 65536 * 3

        if d <= 60:
            return 4000, 65536 * 3

        if d <= 66:
            return 6000, 65536 * 3

        if d <= 74:
            return 10000, 65536 * 3

        if d <= 80:
            return 30000, 65536 * 3

        if d <= 88:
            return 50000, 65536 * 3

        if d <= 94:
            return 60000, 65536 * 9

        return 100000, 65536 * 9

    def siqs_factorise(n):
        dig = len(str(n))
        nf, m = siqs_choose_nf_m(dig)
        factor_base = siqs_factor_base_primes(n, nf)
        required_relations_ratio = 1.05
        success = False
        smooth_relations = []
        prev_cnt = 0
        i_poly = 0
        while not success:
            required_relations = round(len(factor_base) * required_relations_ratio)
            enough_relations = False
            while not enough_relations:
                if i_poly == 0:
                    g, h, B = siqs_find_first_poly(n, m, factor_base)

                else:
                    g, h = siqs_find_next_poly(n, factor_base, i_poly, g, B)

                i_poly += 1
                if i_poly >= 2 ** (len(B) - 1):
                    i_poly = 0

                sieve_array = siqs_sieve(factor_base, m)
                enough_relations = siqs_trial_division(n, sieve_array, factor_base, smooth_relations, g, h, m, required_relations)

                if (len(smooth_relations) >= required_relations or i_poly % 8 == 0 and len(smooth_relations) > prev_cnt):
                    prev_cnt = len(smooth_relations)

            M = siqs_build_matrix(factor_base, smooth_relations)
            M_opt, M_n, M_m = siqs_build_matrix_opt(M)
            perfect_squares = siqs_solve_matrix_opt(M_opt, M_n, M_m)
            factors = siqs_find_factors(n, perfect_squares, smooth_relations)
            if len(factors) > 1:
                success = True

            else:
                required_relations_ratio += 0.05

        return factors

    def check_factor(n, i, factors):
        while n % i == 0:
            n //= i
            factors.append(i)
            if is_prime(n):
                factors.append(n)
                n = 1

        return n

    def trial_div_init_primes(n, upper_bound):
        global small_primes
        is_prime = [True] * (upper_bound + 1)
        is_prime[0:2] = [False] * 2
        factors = []
        small_primes = []
        max_i = sqrt_int(upper_bound)
        rem = n
        for i in range(2, max_i + 1):
            if is_prime[i]:
                small_primes.append(i)
                rem = check_factor(rem, i, factors)
                if rem == 1:
                    return factors, 1

                for j in (range(i ** 2, upper_bound + 1, i)):
                    is_prime[j] = False

        for i in range(max_i + 1, upper_bound + 1):
            if is_prime[i]:
                small_primes.append(i)
                rem = check_factor(rem, i, factors)
                if rem == 1:
                    return factors, 1

        return factors, rem

    def pollard_brent_f(c, n, x):
        x1 = (x * x) % n + c
        if x1 >= n:
            x1 -= n

        return x1

    def pollard_brent_find_factor(n, max_iter = None):
        y, c, m = (randint(1, n - 1) for _ in range(3))
        r, q, g = 1, 1, 1
        i = 0
        while g == 1:
            x = y
            for _ in range(r):
                y = pollard_brent_f(c, n, y)

            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = pollard_brent_f(c, n, y)
                    q = (q * abs(x - y)) % n

                g = gcd(q, n)
                k += m

            r *= 2
            if max_iter:
                i += 1
                if (i == max_iter):
                    return None

        if g == n:
            while True:
                ys = pollard_brent_f(c, n, ys)
                g = gcd(abs(x - ys), n)
                if g > 1:
                    break

        return g


    def pollard_brent_quick(n, factors):
        rem = n
        while True:
            if is_prime(rem):
                factors.append(rem)
                rem = 1
                break

            digits = len(str(n))
            if digits < MIN_DIGITS_POLLARD_QUICK2:
                max_iter = POLLARD_QUICK_ITERATIONS

            else:
                max_iter = POLLARD_QUICK2_ITERATIONS

            f = pollard_brent_find_factor(rem, max_iter)
            if f and f < rem:
                if is_prime(f):
                    factors.append(f)
                    rem //= f

                else:
                    rem_f = pollard_brent_quick(f, factors)
                    rem = (rem // f) * rem_f

            else:
                break

        return rem

    def check_perfect_power(n):
        largest_checked_prime = small_primes[-1]
        for b in small_primes:
            bth_root = kth_root_int(n, b)
            if bth_root < largest_checked_prime:
                break

            if (bth_root ** b == n):
                return (bth_root, b)

        return None


    def find_prime_factors(n):
        perfect_power = check_perfect_power(n)
        if perfect_power:
            factors = [perfect_power[0]]

        else:
            digits = len(str(n))
            if digits <= MAX_DIGITS_POLLARD:
                factors = [pollard_brent_find_factor(n)]

            else:
                factors = siqs_factorise(n)

        prime_factors = []
        for f in set(factors):
            for pf in find_all_prime_factors(f):
                prime_factors.append(pf)

        return prime_factors

    def find_all_prime_factors(n):
        rem = n
        factors = []
        while rem > 1:
            if is_prime(rem):
                factors.append(rem)
                break

            for f in find_prime_factors(rem):
                while rem % f == 0:
                    rem //= f
                    factors.append(f)

        return factors

    def factor(n):
        if type(n) != int or n < 1:
            return 

        if n == 1:
            return []

        if is_prime(n):
            return [n]

        factors, rem = trial_div_init_primes(n, 1000000)
        if rem != 1:
            digits = len(str(rem))
            if digits > MAX_DIGITS_POLLARD:
                rem = pollard_brent_quick(rem, factors)
                
            if rem > 1:
                for fr in find_all_prime_factors(rem):
                    factors.append(fr)

        factors.sort()
        return factors
    
    return factor(n)

def factor_lenstra(n):
    '''
    Return a list that has all factors of n.
    '''
    class Point():
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    class Curve():
        def __init__(self, a, b, m):
            self.a = a
            self.b = b
            self.m = m

    def double_point(P, curve):
        X = P.x
        Y = P.y
        Z = P.z
        a = curve.a
        m = curve.m
        if Y == 0:
            return Point(0, 1, 0)

        if Z == 0:
            return P

        W = a * pow(Z, 2, m) + 3 * pow(X, 2, m)
        S = Y * Z
        B = X * Y * S
        H = pow(W, 2, m) - 8 * B
        X2 = (2 * H * S) % m
        Y2 = (W * (4 * B - H) - 8 * pow(Y, 2, m) * pow(S, 2, m)) % m
        Z2 = pow(2 * S, 3, m)
        return Point(X2, Y2, Z2)

    def add_points(P1, P2, curve):
        if P1.z == 0:
            return P2
        if P2.z == 0:
            return P1
        
        X1 = P1.x
        Y1 = P1.y
        Z1 = P1.z
        X2 = P2.x
        Y2 = P2.y
        Z2 = P2.z
        m = curve.m
        U1 = Y2 * Z1 % m
        U2 = Y1 * Z2 % m
        V1 = X2 * Z1 % m
        V2 = X1 * Z2 % m
        if V1 == V2:
            if U1 == U2:
                return double_point(P1, curve)

            else:
                return Point(0, 1, 0)

        V = (V1 - V2) % m
        U = (U1 - U2) % m
        W = (Z1 * Z2) % m
        A = pow(U, 2, m) * W - pow(V, 3, m) - 2 * pow(V, 2, m) * V2
        X3 = (V * A) % m
        Y3 = (U * (pow(V, 2, m) * V2 - A) - pow(V, 3, m) * U2) % m
        Z3 = (pow(V, 3, m) * W) % m
        return Point(X3, Y3, Z3)

    def multiply_point(P, k, curve):
        if k == 1:
            return P
        
        P2 = Point(0, 1, 0)
        k2 = 0
        
        bit = 1 << (len(bin(k)) - 3)
        
        while k != k2:
            k2 <<= 1
            if k2: 
                P2 = double_point(P2, curve)
            
            if k & bit:
                k2 += 1
                P2 = add_points(P, P2, curve)

            bit >>= 1
            
        return P2

    def factor(n, mode = 1, tries = 10):
        factors = []
        for i in (2, 3):
            while n % i == 0:
                factors.append(i)
                n //= i

        if n == 1:
            return factors

        if is_prime(n):
            factors.append(n)
            factors.sort()
            return factors
        
        max_points = int(2 * n ** 0.25 + n ** 0.5 + 1)
        
        for current_try in range(1, tries + 1):
            a = 0
            b = 0
            while (4 * pow(a, 3, n) + 27 * pow(b, 2, n)) % n == 0:
                x = 1
                y = current_try
                a = randint(1, n - 1)
                b = (pow(y, 2, n) - a * x - pow(x, 3, n)) % n
            
            P = Point(x, y, 1)
            curve = Curve(a, b, n)
            P2 = P
            i = 1
            while True:
                i += 1
                if mode == 0:
                    P2 = add_points(P, P2, curve)

                elif mode == 1:
                    P2 = multiply_point(P2, i, curve)

                elif mode == 2:
                    if i == 2:
                        k = 2
                        k_plus = 4

                    elif i <= 5:
                        k = 2 * i - 3

                    else:
                        k += k_plus
                        k_plus = 6 - k_plus
                    
                    k2 = k
                    while k2 <= max_points:
                        P2 = multiply_point(P2, k, curve)
                        k2 *= k
                
                if P2.z == 0:
                    break

                divisor = gcd(n, P2.z)
                if divisor != 1:
                    divisor2 = n // divisor
                    f2 = factor(divisor, mode, tries)
                    for f in f2:
                        factors.append(f)
                    
                    f2 = factor(divisor2, mode, tries)
                    for f in f2:
                        factors.append(f)
                    
                    factors.sort()
                    return factors
                    
                if i >= max_points:
                    factors.append(n)
                    factors.sort()
                    return factors
        
        factors.append(n)
        factors.sort()
        return factors
    
    return factor(n)

def get_bits(n):
    while True:
        a = getrandbits(n // 2)
        b = getrandbits(n // 2)
        if is_prime(a) and is_prime(b):
            break
    
    return a * b

def test():
    '''A test of this module.'''
    if PRIME_TEST:
        start_tm = time()
        print(f'Twin primes: {find_twins(500)}\n')
        print(f'Palindome primes: {find_palindromes(1000)}\n')
        print(f'Palindome primes which was in base 2: {find_palindromes_base_2(8200)}\n')
        print(f'Reverse primes: {find_reverses(750)}\n')
        print(f'Square palindome primes: {find_square_palindromes(500)}\n')
        print(f'Arithmetic prime progressions: {find_arithmetic_prime_progressions(25)}\n')
        print(f'Mersenne Primes: {find_mersennes(525000)}\n')
        print(f'Double Mersenne Primes: {find_double_mersennes(130)}\n')
        print(f'Fermat Pseudoprime: {find_fermat_pseudoprimes(1000)}\n')
        print(f'Balence Primes: {find_balances(1000)}\n')
        print(f'Carol Primes: {find_carols(4000)}\n')
        print(f'Fibonacci Primes: {find_fibonaccis(1000)}\n')
        print(f'Truncatable Primes (Truncate on left side): {find_truncates(140, LEFT)}\n')
        print(f'Truncatable Primes (Truncate on right side): {find_truncates(295, RIGHT)}\n')
        print(f'Truncatable Primes (Truncate on both sides): {find_truncates(3800, BOTH)}\n')
        print(f'Cuban Primes: {find_cubans(440)}\n')
        print(f'Center Triangular Primes: {find_center_polygons(1000, TRIANGLE)}\n')
        print(f'Center Square Primes: {find_center_polygons(1000, SQUARE)}\n')
        print(f'Center Pentagon Primes: {find_center_polygons(1000, PENTAGON)}\n')
        print(f'Center Hexagon Primes: {find_center_polygons(1000, HEXAGON)}\n')
        print(f'Center Heptagon Primes: {find_center_polygons(1000, HEPTAGON)}\n')
        print(f'Wieferich Primes: {find_wieferiches(3515)}\n')
        print(f'Wilson Primes: {find_wilsons(565)}\n')
        print(f'Happy Primes: {find_happys(195)}\n')
        print(f'Pierpont Primes: {find_pierponts(770)}\n')
        print(f'Leyland Primes: {find_leylands(33000)}\n')
        print(f'Leyland Primes of the second kind: {find_leylands_second_kind(58050)}\n')
        end_tm = time()
        print(f'Prime Test Time: {round(end_tm - start_tm, 12)} seconds.\n')
    
    if FACTOR_TEST:
        start_all = time()
        key_length = 40
        key_large = get_bits(key_length)

        print('Factor of A Large Number Compare Test: \n')
        print('SIQS Method: ')
        start_tm = time()
        print(f'Factor of {key_large}: {factor_siqs(key_large)}')
        end_tm = time()
        print(f'Time: {round(end_tm - start_tm, 12)} seconds.\n')

        print('Lenstra Method: ')
        start_tm = time()
        print(f'Factor of {key_large}: {factor_lenstra(key_large)}')
        end_tm = time()
        print(f'Time: {round(end_tm - start_tm, 12)} seconds.\n')

        key_length = 22
        key_large = get_bits(key_length)

        print('Factor of A Small Number Compare Test: \n')
        print('SIQS Method: ')
        start_tm = time()
        print(f'Factor of {key_large}: {factor_siqs(key_large)}')
        end_tm = time()
        print(f'Time: {round(end_tm - start_tm, 12)} seconds.\n')

        print('Lenstra Method: ')
        start_tm = time()
        print(f'Factor of {key_large}: {factor_lenstra(key_large)}')
        end_tm = time()
        print(f'Time: {round(end_tm - start_tm, 12)} seconds.\n')
        end_all = time()
        print(f'Factor Test Time: {round(end_all - start_all, 12)} seconds.\n')

if __name__ == '__main__':
    if version_info[0] == 3 and version_info[1] >= 6:
        test()
    
    else:
        print('The test method can\'t run in your python version.')