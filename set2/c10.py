import math
import codecs
import base64
from Crypto.Cipher import AES

KEY = "YELLOW SUBMARINE"


def xor(b1 :bytes, b2 :bytes) -> str:
    return ''.join([format(a ^ b, '02x') for a, b in zip(b1, b2)])


def pkcs_7_padding(text_bytes: bytes, block_size: int) -> bytes:
    no_of_blocks = math.ceil(len(text_bytes)/float(block_size))
    pad_value = int(no_of_blocks * block_size - len(text_bytes))

    if pad_value == 0:
        if len(text_bytes) == 0:
            return text_bytes + bytes([block_size]) * block_size
        else:
            return text_bytes
    else:
        return text_bytes + bytes([pad_value]) * pad_value

def pkcs_7_unpadding(input: bytes) -> bytes:
    pad_len = int(input[-1])
    return input[:-pad_len]


def encrypt_cbc(input :bytes, key :str) -> bytes:
    block_length = len(key)
    cipher = pkcs_7_padding(input, block_length)
    previous_text = b''.join([b'\x00' for _ in range(block_length)])
    encipher = AES.new(key, AES.MODE_ECB)
    result = b''
    for i in range(0, len(cipher), block_length):
        cipher_text = encipher.encrypt(bytes.fromhex(
            xor(cipher[i:i+block_length], previous_text)))
        result += cipher_text
        previous_text = cipher_text
    return result


def decrypt_cbc(input :bytes, key :str) -> str:
    block_length = len(key)
    previous_text = b''.join([b'\x00' for _ in range(block_length)])
    decipher = AES.new(key, AES.MODE_ECB)
    result = ''
    for i in range(0, len(input), block_length):
        decrypt_text = bytes.fromhex(
            xor(decipher.decrypt(input[i:i+block_length]), previous_text))
        result += decrypt_text.decode()
        previous_text = input[i:i+block_length]
    return result

def encrypt_cbc2(input :bytes, key :str) -> bytes:
    block_length = len(key)
    cipher = pkcs_7_padding(input, block_length)
    previous_text = b''.join([b'\x00' for _ in range(block_length)])
    decipher = AES.new(key, AES.MODE_CBC, previous_text)
    dec = decipher.decrypt(cipher)
    #dec = pkcs_7_unpadding(dec)
    return dec


if __name__ == '__main__':
    #print(decrypt_cbc(encrypt_cbc(b"YELLOW SUBMARINE", KEY), KEY))
    with open("data/10.txt") as f:
        enc = base64.b64decode(f.read())
    print(decrypt_cbc(enc, KEY))

    print(encrypt_cbc(b"aaaaYELLOW SUBMARINE", KEY))
    print(encrypt_cbc2(b"aaaaYELLOW SUBMARINE", KEY))

    
