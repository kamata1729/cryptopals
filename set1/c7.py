import base64
from Crypto.Cipher import AES

if __name__ == "__main__":
    with open("files/7.txt") as f:
        enc = f.read()
    key = "YELLOW SUBMARINE"
    decipher = AES.new(key, AES.MODE_ECB)

    dec = decipher.decrypt(base64.b64decode(enc)).decode('utf-8').rstrip(chr(0x04))
    print(dec)
