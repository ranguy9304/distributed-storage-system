# Distributed Storage System

This project is an attempt to create a distributed storage system using Python and the socket library. It involves a server and multiple clients that communicate with each other to store and retrieve data.

## Overview

The distributed storage system allows clients to store and retrieve data on the server, which acts as a central coordinator. It manages the distribution of data across multiple clients. When a client sends data to the server, the server distributes this data across the connected clients using a token-based algorithm. Clients can also request data from the server, which then retrieves the data from all connected clients and sends it back to the requesting client.

## Components

### Server

The server is the central component of the system. It:

- Listens for incoming client connections.
- Manages the distribution of data across connected clients.
- Handles requests from clients to retrieve data.

### Client

The client component:

- Connects to the server.
- Can send and receive data. When sending data to the server, the server distributes this data across the connected clients.
- Can request data from the server, which retrieves the data from all connected clients and sends it back.

### Message Classes

Defined in the `msg_classes.py` module, these classes handle the communication between the server and clients. It includes classes for creating and parsing various message types, such as `POST` (for sending data), `FETCH` (for requesting data), and `FETCH_RESP` (for responding to data requests).

### Data Classes

The `data_classes.py` module defines classes for representing the data objects that are stored and retrieved in the system.

### Database Utils

The `db_utils.py` module provides a utility class `SQLStorage` for interacting with an SQLite database. It enables creating tables, inserting data, updating data, retrieving data, and deleting data from the database.

### Settings

The `settings.py` module contains global constants and utility functions used throughout the project.

## Workflow

1. The server starts listening for incoming client connections.
2. Clients connect to the server.
3. When a client sends data to the server, it distributes the data across the connected clients using a token-based algorithm.
4. When a client requests data, the server broadcasts a `FETCH` request to all connected clients.
5. Each client responds with the data it has stored.
6. The server aggregates the data from all clients and sends it back to the requesting client.

## Future Improvements

- Implement data consistency mechanisms to ensure data integrity across multiple clients.
- Explore more efficient and scalable data distribution strategies, such as consistent hashing or distributed hash tables (DHTs).
- Implement security measures, including authentication, authorization, and encryption.
- Add error handling and exception handling mechanisms.
- Implement logging mechanisms for tracking activities, errors, and debug information.
- Add unit tests and integration tests for system correctness and to facilitate future changes and improvements.

## Usage

To run the project, follow these steps:

1. Start the server by running `python server.py`.
2. Start one or more clients by running `python client.py`.
3. In the server terminal, input data to store or type "FETCH" to retrieve data from the clients.
4. In the client terminals, observe the data being received and stored.

**Note:** The project currently uses an in-memory data storage approach. For persistent storage, the code can be modified to integrate with the `db_utils.py` module.
