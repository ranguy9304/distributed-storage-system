import streamlit as st
import json

def display(json_file_path):
    st.title("Distributed Database System")
    st.write("Data collected from clients:")

    # Create a dictionary to store the data for each node
    data_dict = {}

    # Read the JSON data from the file
    with open('dummy_data.json', 'r') as file:
        json_data_list = json.load(file)

    # Process each JSON object
    for json_data in json_data_list:
        # Extract the node, column names, and data from the JSON
        node = json_data["node"]
        column_names = json_data["column_names"]
        data = json_data["data"]

        # Add the data to the corresponding node in the dictionary
        if node not in data_dict:
            data_dict[node] = []
        data_dict[node].append(data)

    # Display the data in a table format
    for node, data_list in data_dict.items():
        st.subheader(f"Node: {node}")
        table_data = [column_names]
        for data in data_list:
            table_data.append(data)
        st.table(table_data)

# Example usage
json_file_path = 'dummy_data.json'
display(json_file_path)