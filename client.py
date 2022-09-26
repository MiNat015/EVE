import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
FORMAT = 'utf-8'
ADDR = (SERVER_HOST, SERVER_PORT)
DISCONNECT = "!DISCONNECT"
separator_token = "<SEP>"

client = socket.socket()

def listen_for_messages():
    while True:
        msg = client.recv(1024).decode()
        print("\n"+msg)


print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
client.connect(ADDR)
print("[+] Connected.")

name = input("Enter your name: ")

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

connected = True

while connected:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send == DISCONNECT:
        connected = False
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    client.send(to_send.encode())

client.close()

