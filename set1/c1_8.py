import codecs
import base64


def discover(enc):
    lines = [bytes.fromhex(line.strip()) for line in enc]
    result = []
    for i in range(len(lines)):
        ciphertext = lines[i]
        for block_size in range(3, 40):
            chunks = [ciphertext[i:i+block_size]
                      for i in range(0, len(ciphertext), block_size)]
            same_num = len(chunks) - len(set(chunks))
            if same_num > 0:
                result.append(
                    {'enc_index': i, 'block_size': block_size, 'same_num': same_num})
    return sorted(result, reverse=True, key=lambda dict: dict['same_num'])[0]

if __name__ == '__main__':
    with open("files/8.txt") as f:
        enc = f.read()
        enc = enc.split('\n')
    
    result = discover(enc)

    print("cipher text: ", enc[result['enc_index']])
    print("block size: ", result['block_size'])    
    
