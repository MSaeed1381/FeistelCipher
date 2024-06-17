from keys import get_processed_keys
from s_box import s_array

keys = get_processed_keys()
MAX_PT_LEN = 64
BOXING_ROUNDS = 32
ADDITION_MOD = pow(2, 32)


def apply_padding(t, max_=MAX_PT_LEN):
    n = len(t)
    if n == max_: return t
    return '0' * (max_ - n) + t


def get_value(t):
    dec_value = int(t[2:], 16)
    bin_value = bin(dec_value)[2:]
    bin_with_padding = apply_padding(bin_value)
    return bin_with_padding


def xor_string(a, b, base_a=2, base_b=2):
    a_n = int(a, base_a)
    b_n = int(b, base_b)
    xor_res = a_n ^ b_n
    bin_xor_res = bin(xor_res)
    return bin_xor_res


def add_string(a, b, base_a=2, base_b=2):
    a_n = int(a, base_a)
    b_n = int(b, base_b)
    add_res = a_n + b_n
    add_res_with_mod = add_res % ADDITION_MOD
    return add_res_with_mod


def get_round_count(n):
    return pow(2, n)


def split_p(p):
    return [p[a: a + 8] for a in range(0, len(p), 8)]


def get_s_box_column(i):
    return int(i[0] + i[6:], 2)


def get_s_box_row(i):
    return int(i[1:6], 2)


def get_s_elements(ps):
    s_elements = []
    for item in ps:
        row = get_s_box_row(item)
        column = get_s_box_column(item)
        s_elements.append(s_array[len(s_elements)][row][column])
    return s_elements


def w(pt):
    ps = split_p(pt)
    s_elements = get_s_elements(ps)
    first_addition = add_string(s_elements[0], s_elements[1], 16, 16)
    xor_ed = xor_string(str(first_addition), s_elements[2], 10, 16)
    res = add_string(xor_ed, s_elements[3], base_b=16)
    bin_res = bin(res)[2:]
    bin_res_with_padding = apply_padding(bin_res, 32)
    return bin_res_with_padding


def final_round(pt, k1, k2):
    l, r = pt[:32], pt[32:]
    l_xor_k1 = xor_string(l, k1, 2, 16)[2:]
    r_xor_k2 = xor_string(r, k2, 2, 16)[2:]
    l_xor_k1_with_padding = apply_padding(l_xor_k1, 32)
    r_xor_k2_with_padding = apply_padding(r_xor_k2, 32)
    return r_xor_k2_with_padding + l_xor_k1_with_padding


def main_round(pt, key):
    l, r = pt[:32], pt[32:]
    l_xor_key = xor_string(l, key, base_b=16)[2:]
    l_xor_key_with_padding = apply_padding(l_xor_key, 32)
    w_result = w(l_xor_key_with_padding)
    w_result_xor_ed_with_right = xor_string(w_result, r, 2, 2)[2:]
    w_result_xor_ed_with_right_with_padding = apply_padding(w_result_xor_ed_with_right, 32)
    return w_result_xor_ed_with_right_with_padding + l


def boxing_rounds(pt, salt):
    for round_ in range(0, BOXING_ROUNDS):
        pt = main_round(pt, keys[round_])
    pt = final_round(pt, keys[-2], keys[-1])
    result = xor_string(pt, salt)[2:]
    result_with_padding = apply_padding(result)
    return result_with_padding


def algorithm(plaintext, salt, work_factor):
    raw_plaintext = get_value(plaintext)
    raw_salt = get_value(salt)
    rounds = get_round_count(work_factor)
    for _ in range(rounds):
        raw_plaintext = boxing_rounds(raw_plaintext, raw_salt)
    return hex(int(raw_plaintext, 2))


def main():
    print("running 4 tests...")

    res = algorithm('0xa0a35e8ca7710', "0xd62af4866aafe96e", 13)
    assert res == '0x6c9ecb88c7a1f4fd'

    res = algorithm('0xa7710', "0x59c394c357335177", 15)
    assert res == '0xeb2da3ee596c65df'

    res = algorithm('0x111111', '0x39c6c1e33ec00e2b', 1)
    assert res == '0x5038d070d6e577b0'

    res = algorithm('0x000000000', '0x701309b2b76e6e2d', 1)
    assert res == '0x13cac2db8d45d664'

    print("all tests passed.")


if __name__ == "__main__":
    main()
