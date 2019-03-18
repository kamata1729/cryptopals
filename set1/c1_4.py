import codecs
import collections

if __name__ == "__main__":
    lines = None
    with open("4.txt") as f:
        lines = f.read()
        lines = lines.split('\n')

    for i, string in enumerate(lines):
        decoded = [x for x in codecs.decode(string.replace('\n', ''), 'hex')]
        key = collections.Counter(decoded).most_common()[0][0] ^ 0x20
        encoded = [x ^ key for x in decoded]
        if min(encoded[:-1]) >= 0x20 and max(encoded[:-1]) <= 0x7a: # 0x20 is space, 0x7a is z
            out = ''.join([format(x ^ key, '02x') for x in decoded])
            print(i, codecs.decode(out, 'hex_codec'))
    
