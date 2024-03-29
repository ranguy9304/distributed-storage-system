POST = "---postdata---"
FETCH = "---fetchdata---"
FETCH_RESP = "---fetchresp---"
SETUP_TABLE = "---setuptable---"
UPDATE = "---updatedata---"
ISALIVE = "---isalive---"
GET = "---getdata---"
GET_RESP = "---getresp---"
DELETE = "---deletedata---"

PORT = 12345
def print_data(data):
    print("---------DATA--------")
    for i in data:
        print(i)
    print("-----------------")
