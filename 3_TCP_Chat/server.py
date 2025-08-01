# chat_server.py
import socket
import threading

HOST = '172.18.16.13'
PORT = 65433
clients = []

def handle_client(conn, addr):
    print(f"[+] {addr} connected.")
    while True:
        try:
            msg = conn.recv(1024)
            if not msg: break
            broadcast(msg, conn)
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"[-] {addr} disconnected.")

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            client.sendall(msg)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server started on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
