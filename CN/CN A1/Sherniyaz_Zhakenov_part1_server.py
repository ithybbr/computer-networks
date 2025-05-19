import socket

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break  # No more data from the client

            print(f"Received from {client_address}: {data.decode()}")
            username = data.decode()
            message = f"Hello {username}! You have successfully logged in!"
            client_socket.sendall(message.encode())
            while True: #a loop to communicate with the client
                data = client_socket.recv(1024)
                received_data = data.decode()
                message = f"Received from {username}: {received_data}"
                print(message)
                client_socket.sendall(message.encode())
                if received_data == "exit message to server":
                    break
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
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
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)
    except KeyboardInterrupt: # handle the keyboard interrupt
        print("\nServer is shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    tcp_server()