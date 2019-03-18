import codecs
INPUT = "1c0111001f010100061a024b53535009181c"
AGAINST = "686974207468652062756c6c277320657965"
ANS = "746865206b696420646f6e277420706c6179"

if __name__ == "__main__":
    output = ''.join([format(a ^ b, 'x') for a, b in zip(
        codecs.decode(INPUT, 'hex'), codecs.decode(AGAINST, 'hex'))])
    print("ANS: ", ANS)
    print("output: ", output)
    print(ANS == output)
