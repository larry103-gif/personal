import math
import time
import random
import sys
from collections import Counter

sys.set_int_max_str_digits(1000000)

# ================= 1. 輔助函數與演算法 =================

def miller_rabin(n):
    """Miller-Rabin 高效質數測試"""
    if n < 2: return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
    if n in small_primes: return True
    if any(n % p == 0 for p in small_primes): return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for a in bases:
        if n <= a: break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def pollard_rho_brent(n):
    """Pollard's Rho - Brent 快速大數分解演算法"""
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    if n % 5 == 0: return 5

    y = random.randint(1, n - 1)
    c = random.randint(1, n - 1)
    m = random.randint(1, n - 1)
    g, r, q = 1, 1, 1

    while g == 1:
        x = y
        for _ in range(r):
            y = (pow(y, 2, n) + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(m, r - k)):
                y = (pow(y, 2, n) + c) % n
                q = (q * abs(x - y)) % n
            g = math.gcd(q, n)
            k += m
        r *= 2

    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = math.gcd(abs(x - ys), n)
            if g > 1: break
    return g

def get_prime_factors(n):
    """取得所有質因數"""
    factors = []
    def factorize(val):
        if val == 1: return
        if miller_rabin(val):
            factors.append(val)
            return
        p = pollard_rho_brent(val)
        factorize(p)
        factorize(val // p)
    factorize(n)
    return sorted(factors)

def get_all_divisors(counts):
    """生成所有正因數"""
    divs = [1]
    for p, e in counts.items():
        new_divs = []
        for d in divs:
            for k in range(1, e + 1):
                new_divs.append(d * (p ** k))
        divs.extend(new_divs)
    return sorted(divs)

def is_perfect_square(n):
    """檢查是否為完全平方數"""
    if n < 0: return False
    r = math.isqrt(n)
    return r * r == n

def to_roman(n):
    """轉換為羅馬數字 (1 <= n <= 3999)"""
    if not (1 <= n <= 3999): return None
    vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman = ""
    for v, s in zip(vals, syms):
        while n >= v:
            roman += s
            n -= v
    return roman

def is_happy_number(n):
    """檢查是否為快樂數 (Happy Number)"""
    seen = set()
    curr = n
    while curr != 1 and curr not in seen:
        seen.add(curr)
        curr = sum(int(d)**2 for d in str(curr))
    return curr == 1

def collatz_steps(n):
    """計算考拉茲猜想 (3n+1) 歸 1 步數"""
    if n <= 0: return None
    steps = 0
    curr = n
    while curr > 1 and steps < 10000:
        if curr % 2 == 0:
            curr //= 2
        else:
            curr = 3 * curr + 1
        steps += 1
    return steps if curr == 1 else "> 10000"

# ================= 2. 順序分析核心功能 =================

def analyze_number(num):
    abs_num = abs(num)
    print("\n" + "=" * 60)
    print(f" 🔍 數字 【 {num} 】 的超級全方位特性分析報告")
    print("=" * 60)

    # 1. 符號與絕對值屬性
    print("\n【 1. 符號與絕對值屬性 】")
    if num > 0:
        sign_str = "正數 (Positive)"
    elif num < 0:
        sign_str = "負數 (Negative)"
    else:
        sign_str = "零 (Zero)"

    print(f"• 數值性質   : {sign_str}")
    print(f"• 絕對值 |N| : {abs_num}")
    print(f"• 相反數 -N  : {-num}")
    if num != 0:
        print(f"• 倒數 1/N   : {1/num:.8f} (即 1/{num})")
    else:
        print("• 倒數 1/N   : 無意義（分母不能為 0）")

    # 2. 位元與數值屬性
    print("\n【 2. 位元與數位屬性 】")
    num_str = str(abs_num)
    digit_len = len(num_str)
    parity = "偶數 (Even)" if num % 2 == 0 else "奇數 (Odd)"
    digit_sum = sum(int(d) for d in num_str)
    bit_len = abs_num.bit_length()
    bit_count = abs_num.bit_count() if hasattr(abs_num, 'bit_count') else bin(abs_num).count('1')

    print(f"• 十進制位數 : {digit_len} 位數")
    print(f"• 奇偶性     : {parity}")
    print(f"• 各數位總和 : {digit_sum}")
    print(f"• 二進制位長 : {bit_len} bits")
    print(f"• 開啟位元數 : {bit_count} 個 (1 的個數 / Hamming Weight)")

    # 3. 進位制與特殊標記 (以絕對值 |N| 為主)
    print("\n【 3. 進位制表示 】")
    prefix = "-" if num < 0 else ""
    print(f"• 二進制 (Binary)      : {prefix}0b{bin(abs_num)[2:]}")
    print(f"• 八進制 (Octal)       : {prefix}0o{oct(abs_num)[2:]}")
    print(f"• 十六進制 (Hex)       : {prefix}0x{hex(abs_num)[2:].upper()}")
    print(f"• 科學記號 (Scientific): {num:.6e}")
    roman = to_roman(abs_num)
    if roman:
        print(f"• 羅馬數字 (|N|)       : {roman}")

    # 4. 質數與質因數分解 (針對絕對值 |N|)
    print("\n【 4. 質數與分解屬性 (|N|) 】")
    if abs_num <= 1:
        print(f"• 質數判定 (|N|) : {abs_num} 既非質數也非合數")
    else:
        is_prime = miller_rabin(abs_num)
        if is_prime:
            print("• 質數判定 (|N|) : ✅ 是質數 (Prime Number)")
            print(f"• 質因數分解     : {abs_num} （本身即為質數）")
        else:
            print("• 質數判定 (|N|) : ❌ 合數 (Composite Number)")
            factors = get_prime_factors(abs_num)
            counts = Counter(factors)
           
            expanded_str = " × ".join(map(str, factors))
            power_str = " × ".join([f"{p}^{c}" if c > 1 else f"{p}" for p, c in counts.items()])
           
            if num < 0:
                print(f"• 質因數連乘     : {num} = -1 × ({expanded_str})")
                print(f"• 標準分解式     : {num} = -1 × ({power_str})")
            else:
                print(f"• 質因數連乘     : {num} = {expanded_str}")
                print(f"• 標準分解式     : {num} = {power_str}")

    # 5. 冪次、根號與對數
    print("\n【 5. 冪次、開方與對數屬性 】")
    print(f"• 平方數 (N²) : {num ** 2}")
    print(f"• 立方數 (N³) : {num ** 3}")

    # 算術平方根
    if num >= 0:
        sqrt_val = math.isqrt(num)
        if sqrt_val * sqrt_val == num:
            print(f"• 平方根 (√N) : {sqrt_val} （完全平方數！）")
        else:
            print(f"• 平方根 (√N) : 約 {math.sqrt(num):.6f} (整數部分: {sqrt_val})")
    else:
        sqrt_abs = math.sqrt(abs_num)
        print(f"• 平方根 (√N) : 約 {sqrt_abs:.6f}i (虛數)")

    # 立方根
    if num >= 0:
        cbrt_val = round(num ** (1/3))
        if cbrt_val ** 3 == num:
            print(f"• 立方根 (∛N) : {cbrt_val} （完全立方數！）")
        else:
            print(f"• 立方根 (∛N) : 約 {num ** (1/3):.6f}")
    else:
        cbrt_val = round(-((-num) ** (1/3)))
        if cbrt_val ** 3 == num:
            print(f"• 立方根 (∛N) : {cbrt_val} （完全立方數！）")
        else:
            print(f"• 立方根 (∛N) : 約 -{(-num) ** (1/3):.6f}")

    # 2 的次方判定
    is_power_of_two = (abs_num > 0) and ((abs_num & (abs_num - 1)) == 0)
    print(f"• 是否為 2 的次方 (|N|): {'是 (2^' + str(abs_num.bit_length() - 1) + ')' if is_power_of_two else '否'}")

    # 对数
    if abs_num > 0:
        print(f"• 常用對數 log10(|N|) : {math.log10(abs_num):.6f}")
        print(f"• 自然對數 ln(|N|)    : {math.log(abs_num):.6f}")
        print(f"• 二進制對數 log2(|N|): {math.log2(abs_num):.6f}")

    # 6. 因數分析 (針對絕對值 |N|)
    print("\n【 6. 因數屬性 (|N|) 】")
    if abs_num > 1:
        if miller_rabin(abs_num):
            counts = {abs_num: 1}
        else:
            factors = get_prime_factors(abs_num)
            counts = Counter(factors)
           
        divisors = get_all_divisors(counts)
        div_count = len(divisors)
        div_sum = sum(divisors)
       
        proper_sum = div_sum - abs_num
        if proper_sum == abs_num:
            perf_status = "完全數 (Perfect Number)"
        elif proper_sum > abs_num:
            perf_status = "盈數 / 豐數 (Abundant Number)"
        else:
            perf_status = "虧數 / 不足數 (Deficient Number)"

        print(f"• 正因數個數 : {div_count} 個")
        print(f"• 正因數總和 : {div_sum}")
        print(f"• 數值類型   : {perf_status}")

        if div_count <= 40:
            print(f"• 所有正因數列表: {divisors}")
        else:
            preview = divisors[:5] + ["..."] + divisors[-5:]
            print(f"• 正因數預覽 : {preview}")

    # 7. 趣味與特殊數列屬性
    print("\n【 7. 特殊數列與趣味數學 】")
    print(f"• 是否為快樂數 (Happy Number): {'✅ 是' if is_happy_number(abs_num) else '❌ 否'}")
    print(f"• 考拉茲猜想 (3n+1) 歸 1 步數 : {collatz_steps(abs_num)}")


# ========== 3. 實際執行呼叫測試 ==========
# 在括號內換上任何你想分析的數字（例如 10 或是 8051）
analyze_number(10)
