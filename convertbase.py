#!/usr/bin/env python
import sys
import string


chars = string.digits+string.ascii_uppercase+string.ascii_lowercase
def convert_to_base_10(no, ibase):
    max_base = len(chars)
    if ibase > max_base or ibase < 2:
        raise Exception('Base not supported')
    data = dict((y,x) for x,y in enumerate(chars))
    ret = 0
    for (i, j) in enumerate(no[::-1]):
        if data[j] >= ibase:
            raise Exception(f'Invalid number: {ibase=} - {data[j]=} {j}')
        ret += ((ibase**i) * data[j])
    return ret



def convert(no, ibase, obase):
    # newno = int(no, ibase)
    if obase > len(chars):
        raise Exception('Output base not supported')
    newno = convert_to_base_10(no, ibase)
    if obase == 10:
        return str(newno)
    data = dict(enumerate(chars))
    ret = []
    while newno:
        ret.insert(0, str(data[newno % obase]))
        newno = int(newno / obase)
    return ''.join(ret)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Invalid number of parameters passed")
        print("Usage:")
        print(sys.argv[0] + " <number> <input_base> <output_base>")
        sys.exit(1)

    print(convert(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])))
