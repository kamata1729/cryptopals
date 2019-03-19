import codecs
import base64
import numpy as np
from c1_3 import single_xor_cipher

def hamming_distance(word1, word2):
    word1_int = int(codecs.encode(word1.encode("utf-8"), 'hex').decode(), 16)
    word2_int = int(codecs.encode(word2.encode("utf-8"), 'hex').decode(), 16)
    return format(word1_int ^ word2_int, 'b').count('1')


def get_keysize():
    scores = []
    for keysize in range(2, 41):
        score = 0
        for i in range(0, len(lines)-keysize, keysize):
            score += hamming_distance(lines[i:i+keysize].decode(),
                                      lines[i+keysize:i+keysize*2].decode()) / keysize
        score = score/len(range(0, len(lines)-keysize, keysize))
        scores.append((keysize, score))
    return sorted(scores, key=lambda tuple: tuple[1])[0][0]

def repeating_xor_cipher(lines, keysize):
    key = ""
    output = []
    line_blocks = ["" for _ in range(keysize)]
    for i, char in enumerate(lines):
        line_blocks[i % keysize] += format(lines[i], '02x')

    for i in range(keysize):
        result_dict = single_xor_cipher(
            line_blocks[i], show_score=True, show_key=True)
        key += result_dict['key']
        output.append(result_dict['output'])

    res = ""
    for i in range(len(lines)):
        res += output[i % keysize][i//keysize]
    return key, res
    

if __name__ == '__main__':
    lines = None
    with open("files/6.txt") as f:
        lines = base64.b64decode(f.read())

    key, result = repeating_xor_cipher(lines, get_keysize())
    print("key: ")
    print(key)
    print("result: ")
    print(result)

    

