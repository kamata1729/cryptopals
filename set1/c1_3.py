import codecs
import collections
import numpy as np

INPUT = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

english_letter_frequency = {
    'e': 12.70,
    't': 9.06,
    'a': 8.17,
    'o': 7.51,
    'i': 6.97,
    'n': 6.75,
    's': 6.33,
    'h': 6.09,
    'r': 5.99,
    'd': 4.25,
    'l': 4.03,
    'c': 2.78,
    'u': 2.76,
    'm': 2.41,
    'w': 2.36,
    'f': 2.23,
    'g': 2.02,
    'y': 1.97,
    'p': 1.93,
    'b': 1.29,
    'v': 0.98,
    'k': 0.77,
    'j': 0.15,
    'x': 0.15,
    'q': 0.10,
    'z': 0.07,
    ' ': 13.00
}


def english_score(input):
    """
    e. g.) input "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    """
    separated = [int(input[2*i: 2*(i+1)], 16)
                 for i in range(len(input)//2)]
    score = 0
    for s in separated:
        if s > 0x7f:
            continue
        char = codecs.decode(format(s, '02x').encode(), 'hex').decode()
        if char in english_letter_frequency.keys():
            score += english_letter_frequency[char]
    return score

if __name__ == "__main__":
    separated = [int(INPUT[2*i: 2*(i+1)], 16)
                 for i in range(len(INPUT)//2)]
    scores = np.zeros(255)
    for i in range(255):
        out = ''.join([format(x ^ i, '02x') for x in separated])
        scores[i] = english_score(out)

    key = scores.argmax()
    output = codecs.decode(''.join([format(x ^ key, '02x') for x in separated]), 'hex').decode()
    print(output)



