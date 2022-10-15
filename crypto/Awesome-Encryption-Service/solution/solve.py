>>> from Crypto.Cipher import AES
>>> first_plain = b'TestTestTestTest'
>>> hex_enc = 'f5f3fea552847c9e5cdf7e6bab576a84'
>>> flag_enc = 'df661cb3c0f4c32a38989ab2104ffec4'
>>> byearray.fromhex(flag_enc)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'byearray' is not defined
>>> bytearray.fromhex(flag_enc)
bytearray(b'\xdff\x1c\xb3\xc0\xf4\xc3*8\x98\x9a\xb2\x10O\xfe\xc4')
>>> bytes(bytearray.fromhex(flag_enc))
b'\xdff\x1c\xb3\xc0\xf4\xc3*8\x98\x9a\xb2\x10O\xfe\xc4'
>>> flag_enc = bytes(bytearray.fromhex(flag_enc))
>>> enc  = bytes(bytearray.fromhex(hex_enc))
>>> enc
b'\xf5\xf3\xfe\xa5R\x84|\x9e\\\xdf~k\xabWj\x84'
>>> [a^b for a,b in zip(enc,first_plain)]
[161, 150, 141, 209, 6, 225, 15, 234, 8, 186, 13, 31, 255, 50, 25, 240]
>>> temp = bytes([a^b for a,b in zip(enc,first_plain)])
>>> [a^b for a,b in zip(flag_enc,temp)]
[126, 240, 145, 98, 198, 21, 204, 192, 48, 34, 151, 173, 239, 125, 231, 52]
>>> bytes([a^b for a,b in zip(flag_enc,temp)])
b'~\xf0\x91b\xc6\x15\xcc\xc00"\x97\xad\xef}\xe74'
>>> hex_enc = '884dfe9cb1e3d0f8d0475cbf959e86ce'
>>> flag_enc = '9546ea8dade7c0e7ff651faf8bcb97c7'
>>> enc  = bytes(bytearray.fromhex(hex_enc))
>>> temp = bytes([a^b for a,b in zip(enc,first_plain)])
>>> first_plain
b'TestTestTestTest'
>>> bytes([a^b for a,b in zip(flag_enc,temp)])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 1, in <listcomp>
TypeError: unsupported operand type(s) for ^: 'str' and 'int'
>>> flag_enc = bytes(bytearray.fromhex(flag_enc))
>>> bytes([a^b for a,b in zip(flag_enc,temp)])
b'IngeHack{G0dJ0b}'
