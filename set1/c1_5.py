import codecs
import collections

INPUT = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
KEY = "ICE"
ANS = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

def decoder(input, key):
    encoded = codecs.encode(input.encode("utf-8"), 'hex')
    encoded = [int(encoded[2*i: 2*(i+1)], 16) for i in range(len(encoded)//2)]
    encoded_key = codecs.encode(key.encode("utf-8"), 'hex')
    encoded_key = [int(encoded_key[2*i: 2*(i+1)], 16)
                   for i in range(len(encoded_key)//2)]
    return ''.join([format(x ^ encoded_key[i % len(encoded_key)], '02x') for i, x in enumerate(encoded)])

if __name__ == "__main__":
    out = decoder(INPUT, KEY)
    print("output: ", out)
    print("answer: ", ANS)
    print(out == ANS)