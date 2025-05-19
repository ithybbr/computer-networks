import socket
import threading
# thread function to be able to both send and receive messages simultaneously
def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            print(data.decode())
    except KeyboardInterrupt: # gracefully exit the client
        return
def tcp_client(client_id, client_password):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = ('localhost', 33333)
    print(f"Client {client_id} connecting to {server_address}")
    client_socket.connect(server_address)

    try:
        # Send data
        message = f"{client_id},{client_password}"
        print(f"Client {client_id} sending: {message}")
        client_socket.sendall(message.encode())

        # Receive response
        data = client_socket.recv(1024)
        if data.decode() == "Invalid credentials!":
            print("Invalid credentials!")
        else:
            print(data.decode())
            try: # creates thread that reads messages from the server
                reading_thread = threading.Thread(target=receive_messages, args=(client_socket,))
                reading_thread.daemon = True
                reading_thread.start()
                while True: # loop to send messages to the server
                    user_input = input()
                    client_socket.sendall(user_input.encode())
            except KeyboardInterrupt: # gracefully exit the client
                return
    finally:
        message = "exit message to server"
        client_socket.sendall(message.encode())
        print("\nExiting...")
        client_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3: # check if the id and password are provided
        print("Usage: python tcp_client.py <client_id>")
        sys.exit(1)
    client_id = sys.argv[1]
    client_password = sys.argv[2]
    tcp_client(client_id, client_password)