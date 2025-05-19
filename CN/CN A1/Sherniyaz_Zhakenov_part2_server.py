import socket
import threading
import json
import time
from time import strftime
clients = {} #dictionary to store client sockets

#a simple hash function to hash the password
def polynomial_hash(s):
    hash_value = 0
    power = 1
    base = 31
    mod = 10**9 + 9
    for char in s:
        hash_value = (hash_value + (ord(char) - ord('a') + 1) * power) % mod
        power = (power * base) % mod
    
    return hash_value

# Function to validate the client credentials
def validate_credentials(client_id, client_password):
    userbase = open("userbase.json", "r")
    users = json.load(userbase)
    if(client_id in users):
        if(users[client_id] == polynomial_hash(client_password)):
            return True
    else:
        return False

# Function to handle each client connection
def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break  # No more data from the client

            print(f"Received from {client_address} at {strftime("%H:%M:%S", time.localtime())}: {data.decode()}")
            username = data.decode().split(",")[0]
            password = data.decode().split(",")[1]

            if(username in clients): #checks if the username is already in the dictionary
                message = "User already logged in!"
                client_socket.sendall(message.encode())
                break
            
            if(validate_credentials(username, password)): # check if the credentials are valid and enters a loop to communicate with the client
                clients[username] = client_socket #adds the client to the dictionary
                message = f"Hello {username}! You have successfully logged in!"
                client_socket.sendall(message.encode())
                while True: #a loop to communicate with the client
                    data = client_socket.recv(1024)
                    received_data = data.decode()
                    print(f"Received from {username} at {strftime("%H:%M:%S", time.localtime())}: {received_data}")
                    if received_data == "exit message to server": #when the client exits they send this message to server to disconnect the client
                        break
                    message = f"[{username}]: {received_data}"
                    for client in clients.values(): #broadcasts the message to all clients
                        if client != client_socket:
                            client.sendall(message.encode())
            else:
                message = "Invalid credentials!"
                client_socket.sendall(message.encode())
            break
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        # Removes the client from the dictionary so that the server does not try to send messages to a disconnected client
        del clients[username]
        # Close the connection
        client_socket.close()
        print(f"Connection with {client_address} closed")


def tcp_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 33333)
    print(f"Starting up on {server_address}")
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)
    print("Waiting for connections...")

    try:
        while True:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()
            # Create a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            print(f"Active connections: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    tcp_server()