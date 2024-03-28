import socket
import threading
from msg_classes import *
import pickle
from db_uitls import *

# Server setup
host = '127.0.0.1'  # Listen on all network interfaces
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, PORT))
server_socket.listen()

clients = []
client_records = {}  # Hashmap to store the number of records in each client
threshold = 5  # Threshold for the difference in the number of records

def broadcast(message, source):
    for client in clients:
        if client != source:
            client.send(message)

def receive():
    while True:
        client, address = server_socket.accept()
        print(f"Connected with {str(address)}")

        clients.append(client)
        client_records[client] = 0  # Initialize the record count for the new client

        # Check if redistribution is needed
        redistribute_records()

def redistribute_records():
    global clients, client_records

    # Check if the difference in the number of records exceeds the threshold
    if len(clients) > 1:
        max_records = max(client_records.values())
        min_records = min(client_records.values())
        if max_records - min_records > threshold:
            # Redistribute the records
            total_records = sum(client_records.values())
            records_per_client = total_records // len(clients)
            extra_records = total_records % len(clients)

            for client in clients:
                target_records = records_per_client
                if extra_records > 0:
                    target_records += 1
                    extra_records -= 1

                if client_records[client] > target_records:
                    # Remove extra records from the client
                    remove_count = client_records[client] - target_records
                    client.send(JsonPacket.REMOVEPacket(remove_count))
                    client_records[client] = target_records
                elif client_records[client] < target_records:
                    # Add missing records to the client
                    add_count = target_records - client_records[client]
                    records_to_add = storage.fetch_records('data', add_count)
                    for record in records_to_add:
                        client.send(JsonPacket.POSTPacket(record))
                    client_records[client] = target_records

def getData():
    while True:
        datain = input("input data to store type FETCH to get data:")
        if datain == "FETCH":
            broadcast(JsonPacket.FETCHPacket(), None)
            temp = []
            for client in clients:
                for objs in JsonPacket(client.recv(1024)).msg:
                    temp.append(objs)
            for objs in storage.fetch_all('data'):
                temp.append(objs)
            print("total data")
            print_data(temp)
            continue

        if datain == "BREAK":
            return

        datain = Data(datain, "data")
        sendMsg = JsonPacket.POSTPacket(datain)
        client_index = sum(client_records.values()) % len(clients)
        client = clients[client_index]
        client.send(sendMsg)
        client_records[client] += 1
        storage.post_data('data', {'id': None, 'type': JsonPacket(sendMsg).type, 'msg': json.dumps(JsonPacket(sendMsg).msg)})

        # Check if redistribution is needed
        redistribute_records()

if __name__ == "__main__":
    storage = SQLStorage('messages.db')
    data_table_schema = 'id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, msg TEXT'
    storage.setup_tables('data', data_table_schema)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    data_thread = threading.Thread(target=getData)
    data_thread.start()