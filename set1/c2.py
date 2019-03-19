INPUT = "1c0111001f010100061a024b53535009181c"
AGAINST = "686974207468652062756c6c277320657965"
ANS = "746865206b696420646f6e277420706c6179"

def xor(b1, b2):
    return ''.join([format(a ^ b, 'x') for a, b in zip(b1, b2)])
    
if __name__ == "__main__":
    output = xor(bytes.fromhex(INPUT), bytes.fromhex(AGAINST))
    print("ANS: ", ANS)
    print("output: ", output)
    print(ANS == output)
