class InvalidPaddingError(Exception):
    pass


def is_valid_padding(input: bytes, max_pad_length: int = 16):
    pad_size = input[-1]
    if pad_size >= max_pad_length-1:
        return True
    try:
        for i in range(1, pad_size):
            if input[-i] != pad_size:
                raise InvalidPaddingError('invalid padding byte was found')
    except InvalidPaddingError as e:
        raise e
    return True

if __name__ == '__main__':
    sample1 = b'ICE ICE BABY\x04\x04\x04\x04'
    sample2 = b'ICE ICE BABY\x05\x05\x05\x05'
    sample3 = b'ICE ICE BABY\x01\x02\x03\x04'

    print('input: {}'.format(sample1))
    try:
        print(is_valid_padding(sample1))
    except InvalidPaddingError:
        print(False)

    print('input: {}'.format(sample2))
    try:
        print(is_valid_padding(sample2))
    except InvalidPaddingError:
        print(False)

    print('input: {}'.format(sample3))
    try:
        print(is_valid_padding(sample3))
    except InvalidPaddingError:
        print(False)
    


