import math
import codecs
import base64
import random
from Crypto.Cipher import AES
from c10 import pkcs_7_padding, encrypt_cbc, decrypt_cbc


def encrypt_ecb(input: bytes, key: str) -> bytes:
    block_length = len(key)
    cipher = pkcs_7_padding(input, block_length)
    encipher = AES.new(key, AES.MODE_ECB)
    res = encipher.encrypt(cipher)
    return res


def decrypt_ecb(input :bytes, key :str) -> str:
    decipher = AES.new(key, AES.MODE_ECB)
    dec = decipher.decrypt(input).decode('utf-8').rstrip(chr(0x04))
    return dec


def generate_random_key(length: int = 16) -> bytes:
    return bytes.fromhex(''.join([format(random.randint(0x30, 0x7e+1), '02x') for _ in range(length)]))


def encryption_oracle(input: str, key_length: int = 16) -> bytes:
    key = generate_random_key(key_length)
    clear_text = chr(0)*random.randint(5, 10) + \
        input + chr(0)*random.randint(5, 10)

    encrypt_rule = random.randint(1, 2)
    if encrypt_rule == 1:
        return encrypt_ecb(clear_text.encode(), key)
    if encrypt_rule == 2:
        return encrypt_cbc(clear_text.encode(), key)

if __name__ == '__main__':
    INPUT = "sample string"
    print(encryption_oracle(INPUT))



