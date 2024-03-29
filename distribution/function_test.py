from server import *

if __name__ == '__main__':
    manager =ComsManager()
    print("Enter name and type of the column in below given format enter DONE when done\nname DATATYPE  \n")
    columns = []
    col_names = {}
    while(True):
        col_str = input("start : ")
        if col_str == "DONE":
            break
        columns.append(col_str)
        vals =col_str.split()
        col_names[vals[0]] = vals[1]
    manager.create_table(columns,col_names)
    