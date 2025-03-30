# Python-scoket-chat
A chat system for linix lovers. Where you can run your own server internall and communicate among group of friends. Currently it is limited to 5 clients but you can update value of "CLIENT_COUNT" according to your requirment. 


## General Overview
It contain 2 program one server and the other one is client. 
- First we run the server and then we run client program that will try to connect to the server using the defined port 9999 using TCP connection. 
- As soon as client get connected to server it will display a connection message and ask client for it's name that name will be used to identify the client message.
- After providing the name client will be free to communicate with server and other clients connected to server.
- Whenever any client send a message to server it is broastcasted to all other clients. And similarly when server send a message it is also broad casted to all other clients.

## Libraries
- socket - To use sockets for connections
- threading - To beind each client with a separate thread

## Server
- 