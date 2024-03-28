import socket
import threading
from msg_classes import *
from db_uitls import *
# Server connection details
host = '127.0.0.1'  # Server's IP address
import pickle

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, PORT))

storage = SQLStorage('messages_cli.db')
    # Define the schema for the 'data' table
    # Here, we're assuming the data have an id and content
# data_table_schema = 'id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, msg TEXT'
#     # Set up the 'data' table
# storage.setup_tables('data', data_table_schema)

data = []

table = TableConf()

def receive():
    while True:
    
        message = client.recv(1024)

        recvMsg=JsonPacket(message)
        
        if recvMsg.type == SETUP_TABLE:
            print(recvMsg.msg.schema_str)
            print(recvMsg.msg.col_names)
            print(recvMsg.msg.columns)
            table = recvMsg.msg
            storage.setup_tables('data',recvMsg.msg.schema_str )

        if recvMsg.type  == FETCH:
 
            datas = JsonPacket.FETCH_RESPPacket(storage.fetch_all('data'))
          
            print("sending data")
            client.send(datas)
    
        elif recvMsg.type == POST:
            data.append(recvMsg.getJson())
            recvMsg.msg['id'] = None
            storage.post_data('data', recvMsg.msg)
            temp = storage.fetch_all('data')
            print(temp)
            # print("Data received")
            # print_data(data)
        elif recvMsg.type == UPDATE:
            # sendMsg = JsonPacket.UPDATEPacket(datain)
            # whereclause = input("input WHERE CLAUSE : ")
            # data.append(JsonPacket(sendMsg).getJson())
            recvMsg.msg['id'] = None
            storage.put_data('data', recvMsg.msg,whereclause)
            temp = storage.fetch_all('data')
            print(temp)
        

receive_thread = threading.Thread(target=receive)
receive_thread.start()


