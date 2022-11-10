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
IpAddr = "localhost"
s = socket.socket()
access_token = '0ffd6eb3150512'


#

def MenuClient():
    while True:
        print("What do you want to do?")
        print("1)Get All Information about the system")
        print("2)Get Cpu Information")
        print("3)Get Ram Information")
        print("4)Get current Disk Information")
        print("5)Get Network Information")
        print("6)Get Geolocalization Information")

        x = 0
        resp = input()
        try:
            x = int(resp)

        except ValueError:
            print("Inserisci un numero valido")
        if(x>0 and x<7):
            return x
        else:
            print("Inserisci un numero valido")
        """if resp == '1':
            return 1
        elif resp == '2':  # CPU
            return 2
        elif resp == '3':
            return 3
        elif resp == '4':
            return 4
        elif resp == '5':
            return 5
        elif resp == '6':
            return 6
        else:
            print("Enter a valid Number")
            time.sleep(2)"""


def Operazioni(client):
    while True:
        res = MenuClient()

        print(res)
        client.send(str(res).encode())
        print("Message Sent!")


        message = client.recv(8192).decode()
        print("Message received!")
        print(message)

        time.sleep(1)  # riga finale prima dell'ultima operazione

        print("Do you Want To close the connection?")
        print("1)Yes")
        print("2)No")
        if CloseConnection(client):
            break


def CloseConnection(client):
    response = input()
    if response == "2":
        return False
    elif response == "1":
        client.close()
        return True



def CreaSocket():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket Successfully created")
    except socket.error as e:
        s.close()
        logging.error(e)


def CreaBind():
    global s
    try:
        s.bind((IpAddr, Port))
        print("Bind Creato")
    except socket.error as e:
        s.close()
        logging.error(e)


def Listen():
    global s
    try:
        print("Now in listening...")
        s.listen(5)
        client, address = s.accept()
        print(f"Connessione accettata con {client.getpeername()}")
        client.send(str(access_token).encode())
        return client, address
    except Exception as e:
        print("Errore nel listen")
        s.close()
        logging.error(e)


def ConnectionMenu() -> bool:
    print("Do you want to accept other connections?")
    print("1)Yes")
    print("2)No")
    risposta = input()
    if risposta == '1':
        return False
    elif risposta == '2':
        return True


def main():
    esisteclient = False
    CreaSocket()
    CreaBind()
    while not esisteclient:
        client, _ = Listen()
        Operazioni(client)
        esisteclient = ConnectionMenu()
    s.close()


"""def cls():
    os.system('cls' if os.name == 'nt' else 'clear')"""


def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
