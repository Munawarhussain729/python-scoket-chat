import socket
import threading

BUFFER_SIZE = 1024
CLIENTS_COUNT = 5

#socket.AF_INET refers to IP4
#socket.SOCK_STREAM refer to use TCP port instead of UDP

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind("localhost", 9999)
server_socket.listen(CLIENTS_COUNT)
print("🟢 Server Started.... Waiting fro users to join.")

clients = {} #Dictionary to track clients
shutdown_flag = threading.Event()

def broadcast(message, sender_scoket=None):
    for client in clients.keys():
        if client != sender_scoket:
            try:
                client.send(message.encode())
            except:
                client.close()
                del clients[client]
    

def handleClient(client):
    try:
        username = client.recv(BUFFER_SIZE).decode()
        client[client] = username
        print(f"🟢 {username} has joined the chat.")
        broadcast(f"🔔 {username} has joined the chat!", client)
        
        while True: 
            message = client.recv(BUFFER_SIZE).decode()
            if not message or message.lower() == "exit":
                print(f"🛑 {username} has left the chat.")
                broadcast(f"🔔 {username} has left the chat.", client)
                break
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", client)
    except ConnectionResetError:
        print(f"⚠ {clients[client]} disconnected unexpectedly.")
    finally:
        client.close()
        del clients[client]
    

#Accept new client and start a separate thread for each one
def accept_clients():
    while not shutdown_flag.is_set():
        try:
            client,address = server_socket.accept
            threading.Thread(target=handleClient, args=(client, address),daemon=True).start()
        except:
            break
    

accept_thread = threading.Thread(target=accept_clients, daemon=True) #Daemon thread
accept_thread.start()

while True:
    admin_message = input()
    if admin_message.lower() == "shutdown":
        print("🔴 Shutting down server...")
        shutdown_flag.set()
        broadcast("🚨 Server is shutting down.")
        for client in list(clients.keys()):
            client.close()
        server_socket.close()
        break
    broadcast(f"Sever: {admin_message}")