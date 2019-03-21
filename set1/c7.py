import base64
from Crypto.Cipher import AES

def decrypt_ecb(input, key):
    """
    input: bytes
    key: string
    return: string
    """
    decipher = AES.new(key, AES.MODE_ECB)
    dec = decipher.decrypt(input).decode('utf-8').rstrip(chr(0x04))
    return dec

if __name__ == "__main__":
    with open("files/7.txt") as f:
        enc = f.read()
    key = "YELLOW SUBMARINE"
    decipher = AES.new(key, AES.MODE_ECB)
    dec = decrypt_ecb(base64.b64decode(enc), key)

    print(dec)

