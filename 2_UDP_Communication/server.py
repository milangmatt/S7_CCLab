# udp_server.py
import socket  # Import socket module

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

# Create a UDP socket (IPv4, UDP)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Bind the socket to the address and port
    s.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}...")

    while True:
        # Wait to receive data and the address it came from
        data, addr = s.recvfrom(1024)  # 1024 bytes max
        message = data.decode()
        print(f"Client ({addr}): {message}")

        # If client says 'exit', end chat
        if message.lower() == 'exit':
            print("Client ended the chat.")
            break

        # Prompt server user for reply
        reply = input("Server: ")

        # Send reply to the client's address
        s.sendto(reply.encode(), addr)

        # If server says 'exit', end chat
        if reply.lower() == 'exit':
            print("Server ended the chat.")
            break
