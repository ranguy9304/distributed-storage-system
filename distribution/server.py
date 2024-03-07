import socket
import threading
from msg_classes import *
import pickle
# Server setup
host = '127.0.0.1'  # Listen on all network interfaces
# port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, PORT))
server_socket.listen()

clients = []
nicknames = []
data = []
token = 0




def broadcast(message, source):
    for client in clients:
        if client != source:
            client.send(message)



def receive():
    while True:
        client, address = server_socket.accept()
        print(f"Connected with {str(address)}")


        clients.append(client)



def getData():
    global token

    while True:
        datain = input("input data to store type FETCH to get data:")
        if(datain == "FETCH"):
            broadcast(JsonPacket.FETCHPacket(), None)
            temp =[]
            for client in clients:

                for objs in JsonPacket(client.recv(1024)).msg:
                    temp.append(objs)
            for objs in data:
                temp.append(objs)
            print("total data")
            print_data(temp)
            continue
        
        if(datain == "BREAK"):
            return
        datain = Data(datain,"data")

        sendMsg = JsonPacket.POSTPacket(datain)
        if token == 0:
            
            data.append(JsonPacket(sendMsg))
        else:

            clients[token-1].send(sendMsg)


        #  distribution algo
        token = (token + 1 )% (len(clients )+1)
        # ----------------




if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    data_thread = threading.Thread(target=getData)
    data_thread.start()

