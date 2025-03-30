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


