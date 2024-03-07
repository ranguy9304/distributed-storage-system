import socket
import threading
from msg_classes import *
# Server connection details
host = '127.0.0.1'  # Server's IP address
import pickle

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, PORT))

data = []



def receive():
    while True:
    
        message = client.recv(1024)

        recvMsg=JsonPacket(message)
        

        if recvMsg.type  == FETCH:
 
            datas = JsonPacket.FETCH_RESPPacket(data)
          
            print("sending data")
            client.send(datas)
    
        elif recvMsg.type == POST:
            data.append(recvMsg)
            print("Data received")
            print_data(data)
        

receive_thread = threading.Thread(target=receive)
receive_thread.start()


