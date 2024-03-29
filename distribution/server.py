import socket
import threading
from distribution.msg_classes import *
import pickle
from distribution.db_uitls import *
# import sleep
import time


# Server setup
# host = '127.0.0.1'  # Listen on all network interfaces
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((host, PORT))
# server_socket.listen()

# clients = []
# nicknames = []
# data = []
# token = 0


# table = TableConf()





def broadcast(message, source):
    for client in clients:
        if client != source:
            try:
                client.send(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                



def receive():
    while True:
        client, address = server_socket.accept()
        print(f"Connected with {str(address)}")
        setupmsg = JsonPacket.SETUPPacket(table)
        client.send(setupmsg)
        clients.append(client)

def isAlive():
    while True:
        time.sleep(2)
        for client in clients:
            try:
                client.send(JsonPacket.ISALIVEPacket())
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                # nickname = nicknames[index]
                # broadcast(f"{nickname} left the chat!".encode('utf-8'), None)
                # nicknames.remove(nickname)
                break


def getData():
    global token

    while True:
        print("COLUMNS AVALIABLE:")
        for i in table.col_names:
            print(i+ "  [ "+table.col_names[i]+" ]")
        datain = input("\ninput data to store type FETCH to get data\n\n")
       
        
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
        
            

        whereclause = ''
        if input_sep_vals[0] == FETCH:
            broadcast(JsonPacket.FETCHPacket(), None)
            temp =[]
            for client in clients:

                for objs in JsonPacket(client.recv(1024)).msg:
                    temp.append(objs)
            for objs in storage.fetch_all('data'):
                temp.append(objs)
            print("total data")
            print_data(temp)
        if input_sep_vals[0] == DELETE:
            whereclause = input("input WHERE CLAUSE : ")
            storage.delete_data('data', whereclause)
            datain_dict['WHERE'] = whereclause
            datain = json.dumps(datain_dict)
            del datain_dict['WHERE']
            sendMsg = JsonPacket.DELETEPacket(datain)
            print(sendMsg)
            broadcast(sendMsg, None)
            temp = storage.fetch_all('data')
            print(temp)
            temp = []
            
        elif input_sep_vals[0] == UPDATE:
            whereclause = input("input WHERE CLAUSE : ")
            datain_dict['WHERE'] = whereclause
            datain = json.dumps(datain_dict)
            del datain_dict['WHERE']
          
            storage.put_data('data', datain_dict,whereclause)
            sendMsg = JsonPacket.UPDATEPacket(datain)
            print(sendMsg)
            broadcast(sendMsg, None)
            
        elif input_sep_vals[0] == GET:
            whereclause = input("input WHERE CLAUSE : ")
            datain_dict['WHERE'] = whereclause
            datain = json.dumps(datain_dict)
            del datain_dict['WHERE']
         
            
            sendMsg = JsonPacket.GETPacket(datain)
            print(sendMsg)
            broadcast(sendMsg, None)
            temp =[]
            for client in clients:
                for objs in JsonPacket(client.recv(1024)).msg:
                    temp.append(objs)
            datat =storage.get_data('data', whereclause)
            print(datat)
            if datat != None:
                for objs in datat:
                    temp.append(objs)
            print("total data")
            print_data(temp)
            continue


        
        elif input_sep_vals[0] == POST:
            if token == 0:
                
                if input_sep_vals[0] == POST:
                    datain = json.dumps(datain_dict)
                    sendMsg = JsonPacket.POSTPacket(datain)
                    data.append(JsonPacket(sendMsg).getJson())
                    datain_dict['id'] = None
                    storage.post_data('data', datain_dict)
                    temp = storage.fetch_all('data')
                    print(temp)
            


            else:
                if input_sep_vals[0] == POST : 
                    datain = json.dumps(datain_dict)
                    sendMsg = JsonPacket.POSTPacket(datain)
                clients[token-1].send(sendMsg)


            # #  distribution algo
            token = (token + 1 )% (len(clients )+1)
            # ----------------



class ComsManager:
    table = TableConf()
    storage = None


    # NETWORK VARS
    host = '127.0.0.1'  # Listen on all network interfaces
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients = []
    nicknames = []
    data = []
    token = 0

    tablesCreated = False

    def __init__(self):
        self.server_socket.bind((self.host, PORT))
        self.server_socket.listen()
        self.clients = []
        self.nicknames = []
        self.data = []
        self.token = 0

    def create_table(self,columns,col_names):
        self.table.columns = columns
        self.table.col_names = col_names
        self.storage = SQLStorage('messages.db')
        
        data_schema_dynamic = 'id INTEGER PRIMARY KEY AUTOINCREMENT, '+ ', '.join(self.table.columns)
        print(data_schema_dynamic)
        print(self.table.col_names)
        self.table.schema_str=data_schema_dynamic
        self.storage.setup_tables('data', data_schema_dynamic)
        self.tablesCreated = True

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        # data_thread = threading.Thread(target=self.manageData)
        # data_thread.start()
        alive_thread = threading.Thread(target=self.isAlive)
        alive_thread.start()
    
    def receive(self):
        while True:
            client, address = self.server_socket.accept()
            print(f"Connected with {str(address)}")
            setupmsg = JsonPacket.SETUPPacket(self.table)
            client.send(setupmsg)
            self.clients.append(client)
    def isAlive(self):
        while True:
            time.sleep(2)
            for client in self.clients:
                try:
                    client.send(JsonPacket.ISALIVEPacket())
                except:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    break
    def broadcast(self,message, source):
        for client in self.clients:
            if client != source:
                try:
                    client.send(message)
                except:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
    def fetchData(self):

        self.broadcast(JsonPacket.FETCHPacket(), None)
        temp =[]
        for client in self.clients:

            for objs in JsonPacket(client.recv(1024)).msg:
                temp.append(objs)
        for objs in self.storage.fetch_all('data'):
            temp.append(objs)
        return temp
    def deteteData(self,datain_dict,whereclause):
        # try : 

        self.storage.delete_data('data', whereclause)
        datain_dict['WHERE'] = whereclause
        datain = json.dumps(datain_dict)
        del datain_dict['WHERE']
        sendMsg = JsonPacket.DELETEPacket(datain)
        # print(sendMsg)
        self.broadcast(sendMsg, None)
        return "success"
        # except Exception as e:
        #     return "OPERATIO FAILED" + e
    def updateData(self,datain_dict,whereclause):
        datain_dict['WHERE'] = whereclause
        datain = json.dumps(datain_dict)
        del datain_dict['WHERE']
    
        self.storage.put_data('data', datain_dict,whereclause)
        sendMsg = JsonPacket.UPDATEPacket(datain)
        print(sendMsg)
        self.broadcast(sendMsg, None)
        return "success"
    def getData(self,datain_dict,whereclause):
        datain_dict['WHERE'] = whereclause
        datain = json.dumps(datain_dict)
        del datain_dict['WHERE']
    
        
        sendMsg = JsonPacket.GETPacket(datain)
       
        self.broadcast(sendMsg, None)
        temp =[]
        for client in self.clients:
            for objs in JsonPacket(client.recv(1024)).msg:
                temp.append(objs)
        datat =self.storage.get_data('data', whereclause)
        
        if datat != None:
            for objs in datat:
                temp.append(objs)
        return temp
    def postData(self,datain_dict):
        if self.token == 0:
            datain = json.dumps(datain_dict)
            sendMsg = JsonPacket.POSTPacket(datain)
            self.data.append(JsonPacket(sendMsg).getJson())
            datain_dict['id'] = None
            self.storage.post_data('data', datain_dict)
         
        else:
            datain = json.dumps(datain_dict)
            sendMsg = JsonPacket.POSTPacket(datain)
            self.clients[self.token-1].send(sendMsg)

        # #  distribution algo
        self.token = (self.token + 1 )% (len(self.clients )+1)
        
        

    def manageData(self):
        while True:
            print("COLUMNS AVALIABLE:")
            for i in self.table.col_names:
                print(i+ "  [ "+self.table.col_names[i]+" ]")
            datain = input("\ninput data to store type FETCH to get data\n\n")
        
            
            if(datain == "BREAK"):
                return
            print(datain)
            input_sep_vals = datain.split(',')
            datain_dict ={}
            print(input_sep_vals)
            for i in input_sep_vals[1:]:
                col_wise_sep = i .split()
                if col_wise_sep[0] not in self.table.col_names:
                    print("COLUMN NOT FOUND, WRONG COLUMN NAME")
                    exit(-1)
                datain_dict[col_wise_sep[0]]= col_wise_sep[1]
            print("\n-----\n")
            print(datain_dict)
            print("\n-----\n")
            
                

            whereclause = ''
            if input_sep_vals[0] == FETCH:
                dataf = self.fetchData()
                print_data(dataf)
                
            if input_sep_vals[0] == DELETE:
                whereclause = input("input WHERE CLAUSE : ")
                datad = self.deteteData(datain_dict,whereclause)
                print(datad)
                
                
            elif input_sep_vals[0] == UPDATE:
                whereclause = input("input WHERE CLAUSE : ")
                datau = self.updateData(datain_dict,whereclause)
                print(datau)
                
                
            elif input_sep_vals[0] == GET:
                whereclause = input("input WHERE CLAUSE : ")
                datag = self.getData(datain_dict,whereclause)
                print_data(datag)
                


            
            elif input_sep_vals[0] == POST:
                datap = self.postData(datain_dict)
                print(datap)

        




if __name__ == "__main__":
    storage = SQLStorage('messages.db')
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
 
    if table.col_names != {}:
        storage.setup_tables('data', data_schema_dynamic)
        
   
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    data_thread = threading.Thread(target=getData)
    data_thread.start()
    alive_thread = threading.Thread(target=isAlive)
    alive_thread.start()

