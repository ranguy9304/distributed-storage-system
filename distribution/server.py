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


table = TableConf()





def broadcast(message, source):
    for client in clients:
        if client != source:
            client.send(message)



def receive():
    while True:
        client, address = server_socket.accept()
        print(f"Connected with {str(address)}")
        setupmsg = JsonPacket.SETUPPacket(table)
        client.send(setupmsg)
        clients.append(client)



def getData():
    global token

    while True:
        print("COLUMNS AVALIABLE:")
        for i in table.col_names:
            print(i+ "  [ "+table.col_names[i]+" ]")
        datain = input("\ninput data to store type FETCH to get data\n\n")
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
        print(datain)
        input_sep_vals = datain.split(',')
        datain_dict ={}
        print(input_sep_vals)
        for i in input_sep_vals[1:]:
            col_wise_sep = i .split()
            if col_wise_sep[0] not in table.col_names:
                print("COLUMN NOT FOUND, WRONG COLUMN NAME")
                exit(-1)
            datain_dict[col_wise_sep[0]]= col_wise_sep[1]
        datain = json.dumps(datain_dict)
            
        # datain = Data.createDataPack(datain,"data")

        
        
        if token == 0:
            if input_sep_vals[0] == POST:
                sendMsg = JsonPacket.POSTPacket(datain)
                data.append(JsonPacket(sendMsg).getJson())
                datain_dict['id'] = None
                storage.post_data('data', datain_dict)
                temp = storage.fetch_all('data')
                print(temp)
            if input_sep_vals[0] == UPDATE:
                sendMsg = JsonPacket.UPDATEPacket(datain)
                whereclause = input("input WHERE CLAUSE : ")
                data.append(JsonPacket(sendMsg).getJson())
                datain_dict['id'] = None
                storage.put_data('data', datain_dict,whereclause)
                temp = storage.fetch_all('data')


        else:
            if input_sep_vals[0] == POST : 
                sendMsg = JsonPacket.POSTPacket(datain)
            if input_sep_vals[0] == UPDATE : 
                sendMsg = JsonPacket.UPDATEPacket(datain)

            clients[token-1].send(sendMsg)


        # #  distribution algo
        token = (token + 1 )% (len(clients )+1)
        # ----------------




if __name__ == "__main__":
    storage = SQLStorage('messages.db')
    
    # Define the schema for the 'data' table
    # Here, we're assuming the data have an id and content
      
    print("Enter name and type of the column in below given format enter DONE when done\nname DATATYPE  \n")
    table.columns = []
    table.col_names = {}
    while(True):
        col_str = input("start : ")
        if col_str == "DONE":
            break
        table.columns.append(col_str)
        vals =col_str.split()
        table.col_names[vals[0]] = vals[1]

    data_schema_dynamic = 'id INTEGER PRIMARY KEY AUTOINCREMENT, '+ ', '.join(table.columns)
    print(data_schema_dynamic)
    print(table.col_names)
    table.schema_str=data_schema_dynamic

    print("input data to store type FETCH to get data \n[ start the query with type EXAMPLE : ---postdata---, colname value, colname value]:\n")
    # data_table_schema = 'id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, msg TEXT'
    # # Set up the 'data' table
    storage.setup_tables('data', data_schema_dynamic)
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

