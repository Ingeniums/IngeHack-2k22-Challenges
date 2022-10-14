
import base64

gate = [118, 88, 312, 164, 525, 672, 721, 352, 405, 1100, 1254, 1128, 1274, 1288, 1635, 1488, 748, 738, 1672, 2020, 1680, 2200, 2070, 2256, 2575]
block = b"SXQwLmd2Mi5IXzQuYzA2LntfOC4zcjEwLmxfMTIuZDAxNC5uXzE2Ll9yMTguZW0yMC5ldDIyLnRkMjQ="
plen = 50



password = [None] * plen
half = [chr(3 * (g + 7 * a) // a // 3) for a, g in enumerate(gate, 1)]
password[::-2] = half
print(password)
ps = base64.b64decode(block).split(b".")
print(ps)
hammer = {i[2:]: i[:2] for i in ps}

for k, v in hammer.items():
    i = int(k)
    first, second = v
    password[i] = chr(first)
    password[i + plen // 2-1] = chr(second)
print(password)
print("".join(password))
