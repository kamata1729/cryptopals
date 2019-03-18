INPUT = "1c0111001f010100061a024b53535009181c"
AGAINST = "686974207468652062756c6c277320657965"
ANS = "746865206b696420646f6e277420706c6179"

if __name__ == "__main__":
    input_separated = [int(INPUT[2*i: 2*(i+1)], 16)
                       for i in range(len(INPUT)//2)]
    against_separated = [int(AGAINST[2*i: 2*(i+1)], 16)
                         for i in range(len(AGAINST)//2)]
    output = ''.join([format(a ^ b, 'x') for a, b in zip(input_separated, against_separated)])
    print("ANS: ", ANS)
    print("output: ", output)
    print(ANS == output)
