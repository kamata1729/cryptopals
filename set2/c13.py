from c10 import *
from c11 import *
from c12 import *
import math
import argparse


def str_to_dict(string):
    obj = {}
    for kv in string.split("&"):
        kv = kv.split("=")
        obj[kv[0]] = kv[1]
    return obj


def profile_for(email) -> bytes:
    """
    email: bytes or str
    return ECB encrypt bytes
    """
    if isinstance(email, bytes):
        email = email.decode()
    email = email.replace("&", "").replace("=", "")
    profile = "email=" + email + "&uid=10&role=user"
    padded_buffer = pkcs_7_padding(profile.encode(), block_size=len(KEY))
    return encrypt_ecb(padded_buffer, KEY)


def dec_profile(profile: bytes) -> bytes:
    return decrypt_ecb(profile, KEY)


def create_admin_profile():
    block_size = detect_cipher_mode(KEY)['block_size']

    # get cipher text of "email=AA....A&uid=10&role=" (length is block_size*N)
    mandatory_str = "email=&uid=10&role="
    all_len = math.ceil(len(mandatory_str) / block_size) * 16
    email_len = all_len - len(mandatory_str)
    email = "A" * email_len
    profile_prefix = profile_for(email)[:all_len]

    # make "email=AA.....Aadmin\x??.....\x??"
    # length of "email=AA.....A" is block_size*N, and length of  "admin\x??.....\x??" is block_size
    # thus, we can get cipher text of  "admin\x??.....\x??"
    mandatory_str = "email="
    all_len = math.ceil(len(mandatory_str) / block_size) * 16
    email_len = all_len - len(mandatory_str)
    email = b'A' * email_len
    email += pkcs_7_padding("admin".encode(), block_size)
    profile_postfix = profile_for(email)[all_len:all_len+block_size]

    # concat above two plain texts
    profile = profile_prefix + profile_postfix
    return profile


if __name__ == '__main__':
    KEY = generate_random_key()
    print("admin email: ", create_admin_profile())
    print("admin account: ", dec_profile(create_admin_profile()))
