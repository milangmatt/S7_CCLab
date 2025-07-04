# udp_client.py
import socket  # Import socket module

HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server port

# Create a UDP socket (IPv4, UDP)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print("Connected to UDP server. Type 'exit' to quit.")

    while True:
        # Get message from client user
        message = input("Client: ")

        # Send the message to the server's address
        s.sendto(message.encode(), (HOST, PORT))

        # If client says 'exit', end chat
        if message.lower() == 'exit':
            print("Client ended the chat.")
            break

        # Receive server's reply
        data, server = s.recvfrom(1024)
        reply = data.decode()
        print(f"Server: {reply}")

        # If server says 'exit', end chat
        if reply.lower() == 'exit':
            print("Server ended the chat.")
            break
