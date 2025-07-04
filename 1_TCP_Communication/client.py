
# client.py
import socket  # Import the socket module for network communication

HOST = '127.0.0.1'  # IP address of the server (localhost)
PORT = 65432        # The port used by the server

# Create a TCP socket (IPv4 + TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to the server at (IP, port)
    print("Connected to server. Type 'exit' to quit.")

    while True:
        # Get message from the client user
        message = input("Client: ")

        # Send the message to the server
        s.sendall(message.encode())

        # If client sends "exit", end the chat
        if message.lower() == "exit":
            print("Client ended the chat.")
            break

        # Receive server's reply
        data = s.recv(1024).decode()
        print(f"Server: {data}")

        # If server replies with "exit", end the chat
        if data.lower() == "exit":
            print("Server ended the chat.")
            break
