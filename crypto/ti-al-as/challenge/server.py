#!/bin/python3
from sage.all import *
import asyncio
import random
from flag import FLAG
import string 



###########################################
#             Server                      #
###########################################

HOST = "127.0.0.1"
PORT = 1337




def generate_keys():
    """
        Function to generate keys for the exchange 

    """
    # generate strong prime 
    p = random_prime(pow(2,512^576))
    # generate the generator 
    q=mod(primitive_root(p),p)
    return p,q


async def receive_message(reader, name):
    """
        Function that receive message from the stdin 

        The function accepts parameters as:
        - @reader the object that allows to read 
        - @name is the name of the connected peer 

    """
    # receive data 
    data = await reader.read(100)
    # decode message 
    message = data.decode()
    print(f"Received {message!r} from {name!r}")
    return message 


async def send_message(writer, message):
    """
        Function to send a message to the client 

        The functin has parameters:
            - @writer the writer object 
            - @message that will be sent 

    """
    print(f"Send: {message!r}")
    writer.write(message.encode())
    await writer.drain()





def xor(message, key):
    return bytes([ m^k for m,k in zip(message,key)])


async def receive_secret_message(reader, name): 
    """
        Function that receive secret message from the stdin 

        The function accepts parameters as:
        - @reader the object that allows to read 
        - @name is the name of the connected peer 

    """
    # receive data 
    data = await reader.read(100)
    length = int(data[:2].decode())
    key = random.randbytes(length)
    secret_message = xor(key,data[2:])
    # decode message 
    print(f"Received {secret_message!r} from {name!r}")
    return secret_message





async def send_secret_messages(writer, message):
    """
            Function to send secret messages 

            The function takes as parameters
                - @writer which is the writer object 
                - @message secret message to send

    """
    print(f"Sending Secret Message '{message}'")
    key = random.randbytes(len(message))
    secret_message = xor(key, message.encode())
    length = str(len(message)).encode()
    writer.write(length+secret_message)
    await writer.drain()



async def handle_connection(reader, writer):
    """
        Function that handle connections, it is triggered once a connection has been set 

        The function accepst as parameters
            - @reader object that allows to read from the stdin 
            - @writer object that allows to write to the stdin 

    """
    # await for data 
    addr = writer.get_extra_info('peername')
    # wait for the connection initiator 
    message  = await receive_message(reader, addr)
    if message == "Hello From Ti-Al-As":
        # connectin initiated 
        q,p = generate_keys()
        message = "p="+str(p)+"&q="+str(q)
        await send_message(writer, message)
        client_secret = await receive_message(reader,addr)
        s1 = randint(1,q)
        server_secret = pow(p,s1,q)
        await send_message(writer, "S="+ str(server_secret))
        secret = int(pow(int(client_secret.split('=')[1]),s1,q))
        random.seed(secret.to_bytes(16,'big'))
    else:
        print("Close the connection")
        writer.close()
    
    secret_message = await receive_secret_message(reader, addr)
    await send_secret_messages(writer, "Yes we are safe now !! ")
    send_flag = await receive_secret_message(reader, addr)
    choice_list = list(range(64))
    random.shuffle(choice_list)
    for elem in choice_list:
        if elem == 22:
            await send_secret_messages(writer,FLAG)
        else:
            import uuid
            await send_secret_messages(writer, str(uuid.uuid4()) )
        message = await receive_secret_message(reader,addr)
        print(message)
    print("Close the connection")
    writer.close()





async def create_server(host,port):
    """
        Function that creates an asyncronous server

        The function accepts a parameters
            - @host that represents the host ip address
            - @port that represents the port of the server 

    """
    # start server 
    server = await asyncio.start_server(handle_connection, host, port)
    # print the addresses
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    return server 




async def main():
    # launch the server 
    server = await create_server(HOST,PORT)
    # make the server wait for ever 
    async with server:
        await server.serve_forever()




if __name__ == "__main__":
    asyncio.run(main())
