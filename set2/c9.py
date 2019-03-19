import math
def pkcs_7_padding(text, block_size):
    no_of_blocks = math.ceil(len(text)/float(block_size))
    pad_value = int(no_of_blocks * block_size - len(text))

    if pad_value == 0:
        return text + chr(block_size) * block_size
    else:
        return text + chr(pad_value) * pad_value

if __name__ == '__main__':
    INPUT = "YELLOW SUBMARINE"
    BLOCK_LENGTH = 20
    print(pkcs_7_padding(INPUT, BLOCK_LENGTH))
    print(pkcs_7_padding(INPUT, BLOCK_LENGTH)
          == 'YELLOW SUBMARINE\x04\x04\x04\x04')
