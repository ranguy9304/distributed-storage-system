import socket
import threading
from msg_classes import *
import pickle
from db_uitls import *
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
            for objs in storage.fetch_all('data'):
                temp.append(objs)
            print("total data")
            print_data(temp)
            continue
        
        if(datain == "BREAK"):
            return
        datain = Data(datain,"data")

        sendMsg = JsonPacket.POSTPacket(datain)
        if token == 0:
            print(JsonPacket(sendMsg).getJson())
            data.append(JsonPacket(sendMsg).getJson())
            print(type(JsonPacket(sendMsg).msg))
            storage.post_data('data', {'id':None, 'type': JsonPacket(sendMsg).type, 'msg': json.dumps(JsonPacket(sendMsg).msg)})
            temp = storage.fetch_all('data')
            print(temp)
        else:

            clients[token-1].send(sendMsg)


        #  distribution algo
        token = (token + 1 )% (len(clients )+1)
        # ----------------




if __name__ == "__main__":
    storage = SQLStorage('messages.db')
    # Define the schema for the 'data' table
    # Here, we're assuming the data have an id and content
    data_table_schema = 'id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, msg TEXT'
    # Set up the 'data' table
    storage.setup_tables('data', data_table_schema)
    # storage.post_data('data', {'id':None, 'type': "hello", 'msg': "my g"})

    # temp = storage.fetch_all('data')
    # print(temp)
    # storage.put_data('data', {'content': "my cdcssdc"}, "id = 1")

    # temp = storage.fetch_all('data')
    # print(type(temp[0]))
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    data_thread = threading.Thread(target=getData)
    data_thread.start()

