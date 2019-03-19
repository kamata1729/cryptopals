def pkcs_7_padding(input, block_length):
    pad_length = block_length % len(input)
    return input + '\\x' + '\\x'.join([format(pad_length, '02x') for _ in range(pad_length)])

if __name__ == '__main__':
    INPUT = "YELLOW SUBMARINE"
    BLOCK_LENGTH = 20
    print(pkcs_7_padding(INPUT, BLOCK_LENGTH))
