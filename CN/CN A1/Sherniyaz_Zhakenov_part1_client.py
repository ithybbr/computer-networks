import socket

def tcp_client(client_id):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = ('localhost', 33333)
    print(f"Client {client_id} connecting to {server_address}")
    client_socket.connect(server_address)

    try:
        # Send data
        message = f"{client_id}"
        print(f"Client {client_id} sending: {message}")
        client_socket.sendall(message.encode())

        # Receive response
        data = client_socket.recv(1024)
        print(data.decode())
        try:
            while True: # loop to communicate with the server in case of successful login
                user_input = input()
                client_socket.sendall(user_input.encode())
                data = client_socket.recv(1024)
                print(data.decode())
        except KeyboardInterrupt: # gracefully exit the client
            return
    finally:
        message = "exit message to server" #when the client exits they send this message to server to disconnect the client
        client_socket.sendall(message.encode())
        print("\nExiting...")
        client_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2: # check if the id is provided
        print("Usage: python tcp_client.py <client_id>")
        sys.exit(1)
    client_id = sys.argv[1]
    tcp_client(client_id)