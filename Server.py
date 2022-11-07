# default imports
import logging
import signal
import socket
import sys
import os
import time
import platform

# downloaded imports


# attributi globali
Port = 41909
IpAddr = "192.168.1.16"
s = socket.socket()




#

def Menu():
    while True:
        print("What do you want to do?")
        print("1)Get All Information about the system")
        print("2)TODO")
        print("3)TODO")
        resp = input()
        if resp == "1":
            return 1
        else:
            break


def Operazioni(client, address):
    while True:
        res = Menu()

        print(res)
        if res == 1:
            client.send(str(res).encode())
            print("Message Sent!")
        else:
            pass

        message = client.recv(8192).decode()
        print("Message received!")
        print(message)

        time.sleep(1)  # riga finale prima dell'ultima operazione
        print("Do you Want To close the connection?")
        print("1)Yes")
        print("2)No")
        response = input()
        if response == "2":
            pass
        elif response == "1":
            client.close()
            break


def CreaSocket():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        s.close()
        logging.error(e)
    print("Socket Successfully created")


def CreaBind():
    global s
    try:
        s.bind((IpAddr, Port))
    except socket.error as e:
        s.close()
        logging.error(e)


def Listen():
    global s
    print("Now in listening...")
    s.listen(5)
    client, address = s.accept()  # la connessione in entrata viene splittata in 2 variabili
    print(f"Connection Established with {client}\n")
    return client, address


def main():
    CreaSocket()
    CreaBind()
    client, address = Listen()
    Operazioni(client, address)
    s.close()
    client.close()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def signal_handler(signal,frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)



if __name__ == "__main__":
    signal.signal(signal.SIGINT,signal_handler)
    main()
