#!/usr/bin/env python
import sys
import string

def convert(no, ibase, obase):
    newno = int(no, ibase)
    if obase == 10:
        return str(newno)
    data = dict(enumerate(string.digits+string.ascii_uppercase))
    ret = []
    while newno:
        ret.insert(0, str(data[newno % obase]))
        newno = int(newno / obase)
    return ''.join(ret)


if len(sys.argv) != 4:
    print("Invalid number of parameters passed")
    print("Usage:")
    print(sys.argv[0] + " <number> <input_base> <output_base>")
    sys.exit(1)

print(convert(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])))
