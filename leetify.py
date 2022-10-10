#!/usr/bin/env python3

import random
import sys

leets = {
    'o': '0',
    'i': '1',
    'e': '3',
    'a': '4',
    's': '$',
}

def leetify(s):
    s = ''.join(random.choice((leets.get(c, c), c)) for c in s)
    return ''.join(random.choice((c.swapcase(), c)) for c in s)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} FLAG_FORMAT FLAG_STRING", file=sys.stderr)
        sys.exit(1)

    flag_format = sys.argv[1]
    flag_string = sys.argv[2]

    flag = f"{flag_format}{{{leetify(flag_string)}}}"

    print(flag)
