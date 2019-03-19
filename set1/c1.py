import codecs
INPUT = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
ANS = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

if __name__ == "__main__":
    output = codecs.encode(codecs.decode(INPUT, 'hex'), 'base64')
    print("out", output.decode())
    print("ANS", ANS)


