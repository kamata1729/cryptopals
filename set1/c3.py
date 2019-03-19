import codecs
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
            score = 0
            break
        char = codecs.decode(format(s, '02x').encode(), 'hex').decode().lower()
        if char in english_letter_frequency.keys():
            score += english_letter_frequency[char]
    return score

def single_xor_cipher(input, show_score=False, show_key=False):
    separated = [int(input[2*i: 2*(i+1)], 16)
                 for i in range(len(input)//2)]

    scores = np.zeros(255)
    for i in range(255):
        out = ''.join([format(x ^ i, '02x') for x in separated])
        scores[i] = english_score(out)
    
    result_dict = {}
    if max(scores) == 0:
        result_dict['output'] = ""
        if show_score:
            result_dict['score'] = 0
        if show_key:
            result_dict['key'] = ""
    else:
        key = scores.argmax()
        output = codecs.decode(
            ''.join([format(x ^ key, '02x') for x in separated]), 'hex').decode()
        result_dict['output'] = output
        if show_score:
            result_dict['score'] = english_score(
                ''.join([format(x ^ key, '02x') for x in separated]))
        if show_key:
            result_dict['key'] = codecs.decode(format(key, '02x'), 'hex').decode()
    return result_dict

if __name__ == "__main__":
    result_dict = single_xor_cipher(INPUT, show_score=True)
    print("output: {}, score: {}".format(result_dict['output'], result_dict['score']))



