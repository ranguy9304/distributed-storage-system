from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple, Union,Dict
from distribution.server import *
app = FastAPI()
manager = ComsManager()
# In-memory storage for the table
table_data = []
table_columns = []

class CreateTableInput(BaseModel):
    columns: List[Tuple[str, str]]

class PostDataInput(BaseModel):
    values: List[Union[str, int]]

class UpdateDataInput(BaseModel):
    values: Dict[str, Union[str, int]]
    where_clause: str


# {
#   "columns": [
#     ["name", "TEXT"],
#     ["num", "TEXT"]
#   ]
# }
@app.post("/create_table")
def create_table(input_data: CreateTableInput):
    global table_columns
    columns = []
    col_names = {}
    for column_name, column_type in input_data.columns:
        if column_name not in table_columns:
            table_columns.append((column_name, column_type))
            columns.append(column_name + " " + column_type) 
            col_names[column_name] = column_type
    manager.create_table(columns, col_names)
    # manager.table.columns.append("id INTEGER PRIMARY KEY")
    
    return {"message": "Table created successfully"}
@app.post("/load_table")
def load_table():
    manager.load_table()
    # for i in manager.table.columns:
    #     print(i)
    del manager.table.col_names['id']
    
    return {"message": "Table loaded successfully"}


# {
#   "values": [
#     "John Doe",
#     "123456"
#   ]
# }
@app.post("/post_data") # implement a method to get table columns data without creating table [ comsmanager]
def post_data(input_data: PostDataInput):
    values = input_data.values
    print(len(values) ,len(manager.table.col_names))
    if len(values) == len(manager.table.col_names):
        datain_dict = {}
        for value, (col_name) in zip(values, manager.table.col_names):
            datain_dict[col_name] = value
        manager.postData(datain_dict)
        # table_data.append(row)
        return {"message": "Data inserted successfully"}
    else:
        return {"error": "Number of values does not match the number of columns"}

@app.get("/fetch_data")
def fetch_data():
    try:
        data = manager.fetchData()
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/get_data")
def get_data(where_clause: str):
    try :
        data = manager.getData(where_clause)
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/get_table_data")
def get_table_data():

    num_items = len( manager.table.columns)
    return {
        "columns":  manager.table.columns,
        "num_items": num_items
    }

@app.put("/update_data")
def update_data(input_data: UpdateDataInput):
    where_clause = input_data.where_clause
    values = input_data.values
    datain_dict = {}
    for column_name, value in values.items():
        datain_dict[column_name] = value
    manager.updateData(datain_dict, where_clause)
    return {"message": "Data updated successfully"}

@app.delete("/delete_data")
def delete_data(where_clause: str):
    manager.deteteData(where_clause)
    return {"message": "Data deleted successfully"}