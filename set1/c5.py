import codecs
import collections

INPUT = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
KEY = "ICE"
ANS = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

def string_to_bytes(string):
    res = codecs.encode(string.encode("utf-8"), 'hex')
    res = hex_to_bytes(res)
    return res

def hex_to_bytes(hex_string):
    return [int(hex_string[2*i: 2*(i+1)], 16) for i in range(len(hex_string)//2)]

def repeating_key_xor(input, key):
    return ''.join([format(x ^ key[i % len(key)], '02x') for i, x in enumerate(input)])

if __name__ == "__main__":
    out = repeating_key_xor(string_to_bytes(INPUT), string_to_bytes(KEY))
    print("output: ", out)
    print("answer: ", ANS)
    print(out == ANS)
