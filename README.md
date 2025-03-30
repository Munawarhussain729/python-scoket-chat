# Python-Socket-Chat

A chat system for Linux lovers. You can run your own server internally and communicate with a group of friends. Currently, it is limited to 5 clients, but you can update the value of `CLIENT_COUNT` according to your requirement.

## General Overview
This project contains two programs: one for the **server** and one for the **client**.

- First, run the **server** program, which will start listening for incoming connections on port `9999` using a TCP connection.
- Then, run the **client** program, which will try to connect to the server on the specified port.
- Once a client successfully connects, it will receive a confirmation message and be prompted to enter a **username**. This username will be used to identify the client in the chat.
- After providing the username, the client is free to communicate with the server and all other connected clients.
- Whenever a client sends a message, it is **broadcasted** to all other clients. Similarly, when the server sends a message, it is also broadcasted to all clients.

## Libraries Used
- `socket` - To establish and manage socket connections.
- `threading` - To handle multiple clients concurrently by assigning each client a separate thread.

## Server Implementation

1. **Setting up the socket** to use IPv4 and TCP protocols:
   ```python
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   ```

2. **Enabling the socket to reuse the same address (IP and port)** even if it is in a `TIME_WAIT` state:
   ```python
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   ```

3. **Binding the socket to a specific address** and starting the server to listen for new connections:
   ```python
   server_socket.bind(("localhost", 9999))
   server_socket.listen(CLIENTS_COUNT)
   ```

4. The server listens for incoming connections, but to **prevent blocking**, each client is assigned a separate thread. These threads are **daemon threads**, which means they automatically terminate when the main program ends:
   ```python
   accept_thread = threading.Thread(target=accept_clients, daemon=True)
   ```

5. **Accepting client connections** in the `accept_clients` function, which keeps running unless the shutdown flag is set:
   ```python
   def accept_clients():
       while not shutdown_flag.is_set():
           try:
               client, address = server_socket.accept()
               threading.Thread(target=handleClient, args=(client,), daemon=True).start()
           except:
               break
   ```

6. **Server shutdown mechanism**: The server listens for admin input, and if the command `shutdown` is entered, it will close all connections and stop the server gracefully:
   ```python
   while True:
       admin_message = input()
       if admin_message.lower() == "shutdown":
           print("\ud83d\udd34 Shutting down server...")
           shutdown_flag.set()
           broadcast("\ud83d\udea8 Server is shutting down.")
           for client in list(clients.keys()):
               client.close()
           server_socket.close()
           break
       broadcast(f"Server: {admin_message}")
   ```

## Client Implementation

1. The client **creates a socket** and attempts to connect to the server:
   ```python
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client_socket.connect(("localhost", 9999))
   ```

2. The client **sends a username** to the server upon connection:
   ```python
   username = input("Enter your username: ")
   client_socket.send(username.encode())
   ```

3. **Receiving messages** in a separate thread to keep listening for messages from the server:
   ```python
   def receive_messages():
       while True:
           try:
               message = client_socket.recv(BUFFER_SIZE).decode()
               if not message:
                   print("⚠ Server disconnected. Exiting chat...")
                   break
               print("\n" + message)
           except:
               break
       client_socket.close()
       exit()
   ```

4. **Handling client message input**: The client can send messages anytime, and typing `exit` will disconnect from the chat:
   ```python
   while True:
       try:
           message = input()
           if message.lower() == "exit":
               client_socket.send(message.encode())
               break
           elif len(message) > 0:
               client_socket.send(message.encode())
       except:
           print("⚠ Server is down. Exiting chat...")
           break
   client_socket.close()
   ```

