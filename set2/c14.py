import base64
import random
import numpy as np
from c10 import *
from c11 import *
from c12 import *


KEY = generate_random_key()
SECRET = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK"


def generate_random_bytes(min_len=10, max_len=50, length=None) -> bytes:
    if not length:
        length = random.randint(min_len, max_len)
    return b''.join([bytes([random.randint(0, 255)]) for _ in range(length)])


def encrypt_ecb_harder(input: bytes, key: str, prefix_length=None, flag=False) -> bytes:
    block_length = len(key)
    random_prefix = generate_random_bytes(length=prefix_length)
    cipher = pkcs_7_padding(random_prefix+input, block_length)
    encipher = AES.new(key, AES.MODE_ECB)
    res = encipher.encrypt(cipher)
    if flag:
        return res, cipher
    return res


def detect_cipher_mode_harder(key: str, min_key_length: int = 10, max_key_length=100) -> dict:
    sample_text = 'A' * min_key_length
    for i in range(max_key_length - min_key_length):
        sample_text += "A"
        cipher_text_bytes = encrypt_ecb_harder(sample_text.encode(), key)
        duplicates = duplicate_list(list(cipher_text_bytes), min_key_length)
        if len(duplicates) > 0:
            block_size = min([j - i for i, j, _ in duplicates])
            return {'mode': 'ECB', 'block_size': block_size}
    return {'mode': 'CBC', 'block_size': None}


def decrypt_secret_string_harder_variable_prefix_length(secret: bytes) -> bytes:
    block_size = detect_cipher_mode_harder(KEY)['block_size']
    if not block_size:
        return "ERROR"
    prefix_size = None
    max_secret_text_size = None

    """
    get max_secret_text_size
    """
    while True:
        plain = bytes([126]) + bytes([127])*block_size * \
            2 + bytes([126])*block_size + secret
        cipher_text = encrypt_ecb_harder(plain, KEY)
        dup = duplicate_list(cipher_text, block_size)
        if len(dup) == 1:
            # include bytes([126]) and bytes([127])
            prefix_size = dup[0][1]+dup[0][2] + block_size
            max_secret_text_size = len(cipher_text) - prefix_size + block_size
            break

    guessed = b''
    As = b'A' * max_secret_text_size

    """
    detect plain text by a word
    """
    cipher_text = None
    for i in range(max_secret_text_size):
        plain = bytes([126]) + bytes([127])*block_size*2 + \
            bytes([126])*block_size + As[:-i-1] + secret
        cipher_prefix_size = 0
        flag = True
        while flag:
            cipher_text = encrypt_ecb_harder(plain, KEY)
            dup = np.array(duplicate_list(cipher_text, block_size))
            dup = sorted(dup, key=lambda x: x[0])
            if len(dup) == 0:
                continue
            elif len(dup) == 1:
                cipher_prefix_size = dup[0][1]+dup[0][2] + block_size
                flag = False
            elif dup[1][0] - dup[0][0] > block_size:
                cipher_prefix_size = dup[0][1]+dup[0][2] + block_size
                flag = False
        cipher_block = cipher_text[cipher_prefix_size:
                                   cipher_prefix_size+max_secret_text_size]

        for j in range(256):
            plain_candidate = bytes([126]) + bytes([127])*block_size*2 + \
                bytes([126])*block_size + As[:-i-1] + guessed + bytes([j])
            candidate_prefix_size = 0
            flag = True
            while flag:
                candidate = encrypt_ecb_harder(plain_candidate, KEY)
                dup = np.array(duplicate_list(candidate, block_size))
                dup = sorted(dup, key=lambda x: x[0])
                if len(dup) == 0:
                    continue
                elif len(dup) == 1:
                    candidate_prefix_size = dup[0][1]+dup[0][2] + block_size
                    flag = False
                elif dup[1][0] - dup[0][0] > block_size:
                    candidate_prefix_size = dup[0][1]+dup[0][2] + block_size
                    flag = False
            if j == 255:
                # get into padding zone
                return guessed[:-1]
            candidate_block = candidate[candidate_prefix_size:
                                        candidate_prefix_size+max_secret_text_size]
            if cipher_block == candidate_block:
                guessed += bytes([j])
                print(guessed)
                break
    return guessed


def decrypt_secret_string_harder_fixed_prefix_length(secret: bytes) -> bytes:
    block_size = detect_cipher_mode_harder(KEY)['block_size']
    if not block_size:
        return "ERROR"
    """
    get prefix_size
    """
    prefix_size = None
    secret_text_size = None
    for i in range(block_size):
        plain = bytes([126])*i + bytes([127])*block_size * \
            2 + bytes([126])*block_size + secret
        cipher_text = encrypt_ecb_harder(plain, KEY, PREFIX_LENGTH)
        dup = duplicate_list(cipher_text, block_size)
        if len(dup) == 1:
            # not include bytes([126]) or bytes([127])
            prefix_size = dup[0][0] - i
            secret_text_size = len(cipher_text) - prefix_size
            break
    print(prefix_size)

    """
    detect plain text by a word
    """
    guessed = b''
    As = b'A' * secret_text_size
    Bs = b'B' * (math.ceil(prefix_size/block_size) * block_size - prefix_size)
    for i in range(secret_text_size):
        plain = Bs + As[:-i-1] + secret
        cipher_text, original_c = encrypt_ecb_harder(
            plain, KEY, PREFIX_LENGTH, True)
        cipher_block = cipher_text[prefix_size +
                                   len(Bs): prefix_size+len(Bs)+secret_text_size]
        #print(original_c[prefix_size+len(Bs) : prefix_size+len(Bs)+secret_text_size])
        #print(original)
        for j in range(256):
            plain_candidate = Bs + As[:-i-1] + guessed + bytes([j])
            candidate, original = encrypt_ecb_harder(
                plain_candidate, KEY, PREFIX_LENGTH, True)
            candidate_block = candidate[prefix_size +
                                        len(Bs): prefix_size+len(Bs)+secret_text_size]
            #print(original[prefix_size+len(Bs) : prefix_size+len(Bs)+secret_text_size])
            #return
            #print(candidate_block)
            if cipher_block == candidate_block:
                guessed += bytes([j])
                print(guessed)
                break
            if j == ord('a'):
                print(original_c[prefix_size+len(Bs): prefix_size+len(Bs)+secret_text_size])
                print(original[prefix_size+len(Bs): prefix_size+len(Bs)+secret_text_size])
                print(cipher_block)
                print(candidate_block)
                return
    return guessed

