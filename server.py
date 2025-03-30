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

def accept_clients():
    return

accept_thread = threading.Thread(target=accept_clients, daemon=True) #Daemon thread
accept_thread.start()