import codecs
import collections

if __name__ == "__main__":
    lines = None
    with open("4.txt") as f:
        lines = f.read()
        lines = lines.split('\n')

    for i, string in enumerate(lines):
        string = string.replace('\n', '')
        separated = [int(string[2*i: 2*(i+1)], 16)
                     for i in range(len(string)//2)]
        key = collections.Counter(separated).most_common()[0][0] ^ 0x20
        decipher = [x ^ key for x in separated]

        # 0x20 is space, 0x7a is z
        if min(decipher[:-1]) >= 0x20 and max(decipher[:-1]) <= 0x7a:
            out = ''.join([format(x ^ key, '02x') for x in separated])
            print(i, codecs.decode(out, 'hex_codec'))
