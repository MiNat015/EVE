import socket
from threading import Thread
import time
from art import *


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5002
ADDR = (SERVER_HOST, SERVER_PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
serparator_token = "<SEP>" 

# Initialize list/set of all connected client's sockets
client_sockets = set()

# create TCP socket
server = socket.socket()

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
server.bind((SERVER_HOST, SERVER_PORT))


def listen_for_client(cs):
    """
    This function keeps listening for a message from 'cs' socket
    Whenever a message is received, broadcast it to all other connected clients

    Args:
        cs (socket): socket
    """
    
    connected = True
    
    while connected:
        try:
            # keep listening for a message from 'cs' socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected 
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP>
            # token with ": " for formatted printing
            msg = msg.replace(serparator_token, ": ")
        
        # Iterate over all connected sockets
        for client in client_sockets:
            client.send(msg.encode())


def start():
    """
    Starts the server
    """
    server.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    run = True
    
    while run:
        # we keep listening for new connections
        client_socket, client_address = server.accept()
        print(f"[+] {client_address} connected")
    
        # add the new connected client to connected sockets
        client_sockets.add(client_socket)
    
        # Start a new thread that listens for each client's messages
        t = Thread(target=listen_for_client, args=(client_socket,))
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
    
        # start the thread
        t.start()


tprint("Server Starting...")
time.sleep(1)
start()