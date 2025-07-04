# server.py
import socket  # Import the socket module to enable network communication

HOST = '127.0.0.1'  # Localhost 
PORT = 65432        # Port number to bind (above 1024 and not in use)

# Create a TCP socket (IPv4 + TCP( using SOCK_STREAM))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))        # Bind the socket to the IP address and port
    s.listen()                  # Start listening for incoming client connections
    print(f"Server listening on {HOST}:{PORT}...")
    
    # Accept a client connection
    conn, addr = s.accept()
    with conn:  # Ensure connection is properly closed after the block
        print(f"Connected by {addr}")  # Show the address of the connected client
        while True:
            # Receive up to 1024 bytes of data from the client
            data = conn.recv(1024).decode()

            # If no data is received, connection is likely closed
            if not data:
                break

            print(f"Client: {data}")  # Display the received message

            # If the client says "exit", end the chat
            if data.lower() == "exit":
                print("Client ended the chat.")
                break

            # Get server's reply from input
            reply = input("Server: ")

            # Send reply back to the client
            conn.sendall(reply.encode())

            # If server sends "exit", end the chat
            if reply.lower() == "exit":
                print("Server ended the chat.")
                break
