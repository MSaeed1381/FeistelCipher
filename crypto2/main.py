def encode(number):
    left, right = number >> 4, number & 0x0f
    for num in range(ROUNDS):
        left, right = right, left ^ feistel(right, num)
    return left << 4 | right


def decode(number):
    left, right = number >> 4, number & 0x0f
    for num in reversed(range(ROUNDS)):
        left, right = right ^ feistel(left, num), left
    return left << 4 | right


def feistel(number, num):
    offset, multiplier = KEYS[num]
    return (number + offset) * multiplier & 0x0f


if __name__ == '__main__':
    ROUNDS = 8
    plain_text = 418
    KEYS = [(12, 155), (18, 99), (17, 24), (19, 26), (15, 4), (19, 67), (16, 169), (11, 159)]

    cipher_text = encode(plain_text)
    print(f'cipher_text: {cipher_text}')
    print(f'original: {decode(cipher_text)}')