import codecs
import collections
INPUT = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

if __name__ == "__main__":
    separated = [int(INPUT[2*i: 2*(i+1)], 16)
                 for i in range(len(INPUT)//2)]
    most_common = collections.Counter(separated).most_common(1)[0][0]
    print("most common charactor: ", hex(most_common))
    print("So {} is assumed to be SPACE code".format(hex(most_common)))
    key = most_common ^ 0x20
    print("SPACE code is 0x20, so encode key is ", hex(key))
    out = ''.join([format(x ^ key, '02x') for x in separated])
    print("decoded string is ", codecs.decode(out, 'hex_codec').decode())

    


