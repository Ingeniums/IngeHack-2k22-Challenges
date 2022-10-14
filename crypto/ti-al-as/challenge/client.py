#!/bin/python3
from sage.all import *
import asyncio  
import random
import string
#####################################################
#               Client                              #
#####################################################

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1337  # The port used by the server


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
        Function to send a message 

        The functin has parameters:
            - @writer the writer object 
            - @message that will be sent 

    """
    print(f"Send: {message!r}")
    writer.write(message.encode())
    await writer.drain()



async def connect(host, port):
    """
        Function to connect to the server 

        The function accepts as parameters
            - @host that represents the host ip address
            - @port that represents the port of the server 
    """ 
    # connect using asyncio 
    reader, writer = await asyncio.open_connection(host, port)
    return reader, writer



async def initiate_connection(writer, reader):
    """
        Function to initiate connection with a server

        The function accepts as parameters 
            - @writer that represents the asyncrounous writer 
    """
    await send_message(writer, "Hello From Ti-Al-As")
    name = writer.get_extra_info('peername')
    # receive the key 
    key = await receive_message(reader, name)
    q,p = [ int(part.split('=')[1]) for part in  key.split('&')]
    print(q,p)
    # generate random secreat 
    s1 = randint(1,p)
    client_secret = pow(q,s1,p)
    await send_message(writer, 'S='+str(client_secret))
    server_secret = await receive_message(reader,name)
    secret = int(pow(int(server_secret.split('=')[1]), s1,p))
    random.seed(secret.to_bytes(16,'big'))




def xor(message, key):
    return bytes([ m^k for m,k in zip(message,key)])






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



async def main():       
    # first we connect to the server 
    r,w = await connect(HOST,PORT)
    # we initiate a connection 
    await initiate_connection(w,r)
    await send_secret_messages(w,'Are we safe now ??')
    response = await receive_secret_message(r,"safe server")
    await send_secret_messages(w, 'Now send flag !')
    choice_list = list(range(64))
    random.shuffle(choice_list)
    for elem in choice_list:
        message = await receive_secret_message(r,'safe server')
        print(message)
        await send_secret_messages(w, 'message received')

    



if __name__ == "__main__":
    asyncio.run(main())
