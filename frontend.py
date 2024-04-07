import streamlit as st 
import requests

# Function to create table on the backend
def create_table(column_name_input, column_type_input):
    # Backend API endpoint for creating table
    endpoint = "http://127.0.0.1:8000/create_table"
    
    # Prepare the payload for the request
    payload = {
        "columns": [[name, datatype] for name, datatype in zip(column_name_input, column_type_input)]
    }
    print(payload)
    # Send POST request to the backend
    response = requests.post(endpoint, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        return True
    else:
        return False

# Function to fetch table data from FastAPI endpoint
def get_table_data():
    endpoint = "http://127.0.0.1:8000/get_table_data"  # Replace with your FastAPI endpoint
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch table data. Error {response.status_code}: {response.text}")
        return {"columns": [], "num_items": 0}
    
# Function to post data to the backend

def post_data(data_values):
    # Define the API endpoint for posting data
    endpoint = "http://127.0.0.1:8000/post_data"
    
    # Send a POST request to the backend
    response = requests.post(endpoint, json=data_values)
    
    # Check if the request was successful
    if response.status_code == 200:
        return True
    else:
        return False

import streamlit as st
import requests

import streamlit as st
import requests

# Function to fetch table data from FastAPI endpoint
def fetch_table_data():
    endpoint = "http://127.0.0.1:8000/fetch_data"  # Replace with your FastAPI endpoint
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        st.error(f"Failed to fetch table data. Error {response.status_code}: {response.text}")
        return []

def get_data(where_clause: str):
    # Define the endpoint URL
    endpoint = "http://127.0.0.1:8000/get_data"

    # Prepare the request data
    params = {"where_clause": where_clause}

    # Send GET request to the backend
    response = requests.get(endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the data from the response
        return response.json()
    else:
        # Return an error message
        return {"error": f"Failed to fetch data. Error {response.status_code}: {response.text}"}




st.title("Distributed Storage System")
submitted0=0
submitted1=0
submitted2=0
submitted3=0
submitted4=0
submitted1=0
my_form = st.form(key="form1")
column_name_input = []
column_type_input = []
with my_form:
    num_columns = st.number_input("Number of Columns:", min_value=1, step=1)
    submitted0 = st.form_submit_button('Submit 0')

col1, col2 = st.columns(2)
with col1:
    if num_columns==1:
        with st.form('Form1'):
            name1 = st.text_input(label="Name of column:")
            dt1 = st.text_input(label="Type of column:")
            submitted1 = st.form_submit_button('Submit 1')
            column_name_input.append(name1)
            column_type_input.append(dt1)
    if num_columns==2:
        with st.form('Form1'):
            name1 = st.text_input(label="Name of column:")
            dt1 = st.text_input(label="Type of column:")
            submitted1 = st.form_submit_button('Submit 1')
            column_name_input.append(name1)
            column_type_input.append(dt1)

    if num_columns==4 or num_columns==3:
        with st.form('Form1'):
            name1 = st.text_input(label="Name of column:")
            dt1 = st.text_input(label="Type of column:")
            submitted1 = st.form_submit_button('Submit 1')
            column_name_input.append(name1)
            column_type_input.append(dt1)
        with st.form('Form3'):
            name3 = st.text_input(label="Name of column:")
            dt3 = st.text_input(label="Type of column:")
            submitted3 = st.form_submit_button('Submit 3')
            column_name_input.append(name3)
            column_type_input.append(dt3)

with col2:
    if num_columns==2:
        with st.form('Form2'):
            name2 = st.text_input(label="Name of column:")
            dt2 = st.text_input(label="Type of column:")
            submitted2 = st.form_submit_button('Submit 1')
            column_name_input.append(name2)
            column_type_input.append(dt2)
    if num_columns==3:
        with st.form('Form2'):
            name2 = st.text_input(label="Name of column:")
            dt2 = st.text_input(label="Type of column:")
            submitted2 = st.form_submit_button('Submit 1')
            column_name_input.append(name2)
            column_type_input.append(dt2)
    if num_columns==4:
        with st.form('Form2'):
            name2 = st.text_input(label="Name of column:")
            dt2 = st.text_input(label="Type of column:")
            submitted2 = st.form_submit_button('Submit 2')
            column_name_input.append(name2)
            column_type_input.append(dt2)
        with st.form('Form4'):
            name4 = st.text_input(label="Name of column:")
            dt4 = st.text_input(label="Type of column:")
            submitted4 = st.form_submit_button('Submit 4')
            column_name_input.append(name4)
            column_type_input.append(dt4)

flag=0
    # Process form submissions
for i in range(num_columns): 
    if column_name_input[i]=="" :
        flag=1
        break
    print(column_name_input)
    print(column_type_input)
    

if flag==0:
    create_table(column_name_input, column_type_input)
    st.success(f" table created successfully")
    # Fetch table data from FastAPI endpoint
    table_info = get_table_data()

    # Display table information
    st.title("Table Information")
    st.write("Columns:", table_info["columns"])
    st.write("Number of Items:", table_info["num_items"])
st.subheader("Post Data")
# Create input fields for data corresponding to each column
my_form1 = st.form(key="form12")
value=""
with my_form1:  
    data_values1 = []
    for name, datatype in zip(column_name_input, column_type_input):
        if datatype == "TEXT":
            value = st.text_input(f"Enter value for {name}")
        elif datatype == "INTEGER":
            value = st.number_input(f"Enter value for {name}", step=1)
        elif datatype == "FLOAT":
            value = st.number_input(f"Enter value for {name}", step=0.1)
        elif datatype == "DATE":
            value = st.date_input(f"Enter value for {name}")
        data_values1.append(value)
    data_values={"values":data_values1}

# Post data button
    if st.form_submit_button('POST DATA'):
        print(data_values)
        # Post data to backend
        post_data(data_values)
        # Replace this with actual post data logic
        st.success("Data posted successfully!")
        table_data = fetch_table_data()
        print(table_data)
        # Display table data in a tabular format
        st.title("Table Data")
        if table_data:
            # Display table with column names
            data_with_header = [['ID','NODE ID']+column_name_input] + table_data
            st.table(data_with_header)
        else:
            st.write("No data available.")
        # Group table data by node ID
        data_by_node_id = {}

        # Assuming the second element of each row in table_data represents the node ID
        for row in table_data:
            if not row:  # Skip empty rows
                continue
            if len(row) < 2:  # Skip rows that don't have at least two elements
                continue
            node_id = row[1]  # Access the second element of the row
            if node_id not in data_by_node_id:
                data_by_node_id[node_id] = []
            data_by_node_id[node_id].append(row)

        # Display rows grouped by node ID as tables
        st.title("Table Data Grouped by Node ID")
        for node_id, rows in data_by_node_id.items():
            st.header(f"Node ID: {node_id}")
            st.table(rows)

        # Streamlit code for user input
    st.title("Fetch Data")
    where_clause = st.text_input("Enter WHERE clause:", "")

    if st.form_submit_button('fetch DATA'):
        # Call the get_data function with the user-provided WHERE clause
        data = get_data(where_clause)
        if "error" in data:
            st.error(data["error"])
        else:
            st.write("Fetched Data:")
            st.write(data)
