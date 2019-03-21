import math
import codecs
import base64
from Crypto.Cipher import AES

KEY = "YELLOW SUBMARINE"


def xor(b1 :bytes, b2 :bytes):
    return ''.join([format(a ^ b, '02x') for a, b in zip(b1, b2)])


def pkcs_7_padding(text :str, block_size :int) -> str:
    no_of_blocks = math.ceil(len(text)/float(block_size))
    pad_value = int(no_of_blocks * block_size - len(text))

    if pad_value == 0:
        return text + chr(block_size) * block_size
    else:
        return text + chr(pad_value) * pad_value


def encrypt_cbc(input :bytes, key :str) -> bytes:
    block_length = len(key)
    cipher = pkcs_7_padding(input.decode(), block_length).encode()
    previous_text = (''.join(["\x00" for _ in range(block_length)])).encode()
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
    previous_text = (''.join(["\x00" for _ in range(block_length)])).encode()
    decipher = AES.new(key, AES.MODE_ECB)
    result = ''
    for i in range(0, len(input), block_length):
        decrypt_text = bytes.fromhex(
            xor(decipher.decrypt(input[i:i+block_length]), previous_text))
        result += decrypt_text.decode()
        previous_text = input[i:i+block_length]
    return result


if __name__ == '__main__':
    #print(decrypt_cbc(encrypt_cbc(b"YELLOW SUBMARINE", KEY), KEY))
    with open("data/10.txt") as f:
        enc = base64.b64decode(f.read())
    print(decrypt_cbc(enc, KEY))

    
