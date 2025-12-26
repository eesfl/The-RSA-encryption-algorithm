import secrets

def text_to_num(text):
    res = 0
    for char in text:
        res = res*256 + ord(char)
    return res

def num_to_text(num):
    text = ''
    while num > 0:
        text = chr(num %256) + text
        num //= 256
    return text

def encryption(orig_text, e, N):
    enc_text = pow(orig_text, e, N)
    return enc_text

def decryption(enc_text, d, N):
    dec_text = pow(enc_text, d, N)
    return dec_text

def quick_prime_check(n):
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for i in small_primes:
        if n % i == 0:
            return False
    return True

def miller_rabin(n, k):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2 
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def keygen(keylen, k):
    pq_len = keylen // 2
    while True:
        key = secrets.randbits(pq_len)
        key |= (1 << pq_len - 1)
        key |= 1
        if miller_rabin(key, k):
            return key

if __name__ == "__main__":
    original_text = str(input('Введите текст, который хотите зашифровать\n'))
    key_len = int(input('Введите желаемую длину ключа N:\n'))
    p = keygen(key_len, 50)
    q = keygen(key_len, 50)
    N = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e, -1, phi)

    numeric_representation_of_text = text_to_num(original_text)

    print(f"Числовое представление исходного сообщения: {numeric_representation_of_text}")

    encryption_text = encryption(numeric_representation_of_text, e, N)

    print(f"Зашифрованное сообщение в числовом представлении: {encryption_text}.\nЗашифрованное сообщение в текстовом представлении: {num_to_text(encryption_text)}")

    decryption_text = decryption(encryption_text, d, N)

    print(f"Дешифрованное сообщение в числовом представлении: {decryption_text}.\nДешифрованное сообщение в текстовом представлении: {num_to_text(decryption_text)}")

