import codecs
from c1_3 import *

if __name__ == "__main__":
    lines = None
    with open("files/4.txt") as f:
        lines = f.read()
        lines = lines.split('\n')
    
    outputs = []
    scores = []
    for i, string in enumerate(lines):
        string = string.replace('\n', '')
        output, score = single_xor_cipher(string, show_score=True)
        scores.append(score)
    likely_line_index = np.array(scores).argmax()
    print(single_xor_cipher(lines[likely_line_index]))
