import socket
import threading

BUFFER_SIZE = 1024


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(("localhost",9999))

username = input("Enter your user name: ")
client_socket.send(username.encode())
print("🟢 Connected to chat server! Type 'exit' to leave.")


def receive_messages():
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if not message:
                print("⚠ Server disconnected. Exiting chat...")
                break
            if message == "⚠ Server is shutting down.":
                print(message)
                break
            print("\n" + message)
        except ConnectionResetError:
            print("⚠ Connection lost! Server might have shut down.")
            break
        except:
            break
    client_socket.close()  # Ensure client socket is closed properly
    exit()

receiving_thread = threading.Thread(target=receive_messages, daemon=True)
receiving_thread.start()

# User can send messages anytime 
while True:
    try:
        message = input()
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        elif len(message)>0:
            client_socket.send(message.encode())
    except(BrokenPipeError, OSError):
        print("⚠ Server is down. Exiting chat...")
        break
    except ValueError:
        print("⚠ Input error! Exiting...")
        break
    
client_socket.close()
print("🔴 Disconnected from chat.")