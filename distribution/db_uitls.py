import sqlite3

class TableConf:
    def __init__(self):
        self.columns = None
        self.col_names =None
        self.schema_str =None
    # columns = None
    # col_names =None
    # schema_str =None 

class SQLStorage:
    def __init__(self, db_name):
        self.db_name = db_name

    def _connect(self):
        """Create a database connection."""
        return sqlite3.connect(self.db_name)

    def setup_tables(self, table_name, schema):
        """Set up tables in the database."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
        conn.commit()
        conn.close()

    def post_data(self, table_name, data):
        """Insert data into the table."""
        conn = self._connect()
        cursor = conn.cursor()
        #  if data is a dict then execute a code
        if isinstance(data, dict):
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cursor.fetchall()]

            # Extract the values from the data dictionary in the order of columns
            data = [data[column] for column in columns]
        placeholders = ', '.join('?' * len(data))
        # print(placeholders)
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def put_data(self, table_name, data, condition):
        """Update data in the table based on a condition."""
        conn = self._connect()
        cursor = conn.cursor()
        set_clause = ', '.join([f"{k} = ?" for k in data])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        cursor.execute(query, list(data.values()))
        conn.commit()
        conn.close()

    def get_data(self, table_name, condition):
        """Fetch data from the table based on a condition."""
        conn = self._connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def delete_data(self, table_name, condition):
        """Delete data from the table based on a condition."""
        conn = self._connect()
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def fetch_all(self, table_name):
        """Fetch all records from the table."""
        conn = self._connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    def get_columns(self, table_name):
        """Return the column names and their types in a list and a dictionary."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        column_info = cursor.fetchall()
        conn.close()

        print(column_info)

        column_names = [column[1] + " " + column[2] for column in column_info]
        column_types = {column[1]: column[2] for column in column_info}

        return column_names, column_types


def manage_products():
    # Initialize the SQLStorage class with the database file name
    storage = SQLStorage('my_products_database.db')

    # Define the schema for the 'products' table
    # Here, we're assuming products have an id, name, and price
    products_table_schema = 'id INTEGER PRIMARY KEY, name TEXT, price REAL'

    # Set up the 'products' table
    storage.setup_tables('products', products_table_schema)

    # Insert a new product into the 'products' table
    # Note: Passing None for the id as it's auto-incremented
    storage.post_data('products', (None, 'Coffee Mug', 9.99))
    print("Inserted a new product.")

    # Update the price of the 'Coffee Mug' product
    storage.put_data('products', {'price': 12.99}, "name = 'Coffee Mug'")
    print("Updated the price of 'Coffee Mug'.")

    # Retrieve the data of the 'Coffee Mug' product
    coffee_mug = storage.get_data('products', "name = 'Coffee Mug'")
    print(f"Retrieved data for 'Coffee Mug': {coffee_mug}")

    # Fetch all products
    all_products = storage.fetch_all('products')
    print("All products in the database:")
    for product in all_products:
        print(product)

    # Delete the 'Coffee Mug' product
    storage.delete_data('products', "name = 'Coffee Mug'")
    print("Deleted 'Coffee Mug' from the products table.")

# Run the example function


def test():
    storage = SQLStorage('my_database.db')
    # Define the schema for the 'data' table
    # Here, we're assuming the data have an id and content
    data_table_schema = 'id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, description TEXT'
    # Set up the 'data' table
    storage.setup_tables('data', data_table_schema)
    storage.post_data('data', {'id':None, 'content': "hello", 'description': "my g"})

    temp = storage.fetch_all('data')
    print(temp)
    storage.put_data('data', {'content': "my cdcssdc"}, "id = 1")

    temp = storage.fetch_all('data')
    print(type(temp[0]))

# Example usage
# if __name__ == "__main__":
#     test()