from c11 import *
from c10 import *
from Crypto.Cipher import AES
import math
import codecs
import base64
import random

KEY = generate_random_key()

SECRET = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK"


def duplicate_list(lis, min_length: int) -> list:
    """
    detect duplicate part in lis
    return [[start_index_1, start_index_2, length]]
    """
    result = []
    for a in set(lis):
        indices = [i for i, x in enumerate(lis) if x == a]
        if len(indices) > 1:
            for i in range(len(indices) - 1):
                for j in range(i+1, len(indices)):
                    k = 0
                    duplicate_flag = False
                    while lis[indices[i]: indices[i] + min_length+k] == lis[indices[j]: indices[j] + min_length+k]:
                        duplicate_flag = True
                        k += 1
                    if duplicate_flag:
                        result.append([indices[i], indices[j], min_length+k-1])
    return result


def detect_cipher_mode(key: str, min_key_length: int = 10, max_key_length=100) -> dict:
    sample_text = 'A' * min_key_length
    for i in range(max_key_length - min_key_length):
        sample_text += "A"
        cipher_text_bytes = encrypt_ecb(sample_text.encode(), key)
        duplicates = duplicate_list(list(cipher_text_bytes), min_key_length)
        if len(duplicates) > 0:
            block_size = min([j - i for i, j, _ in duplicates])
            return {'mode': 'ECB', 'block_size': block_size}
    return {'mode': 'CBC', 'block_size': None}


def get_secret_string_size(secret: bytes, block_size: int) -> int:
    secret_cipher_length = len(encrypt_ecb(
        pkcs_7_padding(secret, block_size), KEY))
    i = 0
    while True:
        i += block_size
        As = b'A'*i
        as_length = len(encrypt_ecb(As, KEY))
        if as_length == secret_cipher_length:
            return i


def decrypt_secret_string(secret: bytes):
    ciper_property = detect_cipher_mode(KEY)
    if ciper_property['mode'] != 'ECB':
        return -1
    block_size = ciper_property['block_size']
    secret_pad = pkcs_7_padding(secret, block_size)
    secret_string_size = get_secret_string_size(secret, block_size)
    As = b'A' * secret_string_size
    guessed = b''
    old_i = -1
    for i in range(secret_string_size):
        plain_text = As[:-i-1] + secret_pad
        ct_block = encrypt_ecb(plain_text, KEY)
        for j in range(256):
            plain_candidate = As[:-i-1] + guessed + bytes([j])
            candidate = encrypt_ecb(plain_candidate, KEY)
            if ct_block[:secret_string_size] == candidate[:secret_string_size]:
                guessed += bytes([j])
                break
    return guessed

if __name__ == '__main__':
    decrypt_plain_text = decrypt_secret_string(base64.b64decode(SECRET))
    print(decrypt_plain_text.decode())
