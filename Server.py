#  Progetto Reti - The Phantom Thieves of Hearts (Take your time)
#
#
#
#
#                                                                     ,,,,,,,,,,,
#                                                              ,,,,,,,,,,,,
#                                                         ,,,,,,,,,,,,, ,,,   ,
#                                                    ,,,,,,,,,,,,,,, ,, ,,,    ,
#                                                 ,,,,,,,,,,,,,,,,,,,,, ,,,, , ,
#                                              ,,,,,,,,,,,,,,,,,,,,,,,,, ,,,   ,.
#                                             ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ,,,
#                                           ,,,,,,,,,,,,,   ,,,,,,,,,,,,, ,,,,  ,
#                                           ,,,,,,,,,         ,,,,,,,,,,,, ,,,  ,,
#                                                            , ,,,,,,,,,,,,.,,,  ,
#                                                             ,,,,,,,,,,,,,,,,,, ,,                        @
#                                                               , ,,,,,,,,,,,,,,           ,
#                                                                , ,,,,,,,,,,, ,      ,,                      @@
#                                                                   ,,,,,,,,,,  ,, ,,        @@       ,     @
#                                                                    ,,,,,,, ,,,,,,      &@@   ,,,,,,,,   @@
#                                                                      ,, ,,,,,,,      @@@@ ,,,, @ ,,,  @@@
#                                                                     ,,,,,,, ,      @@@@@@,,,,@@ ,,,@@@@@
#                                                                 ,,,,,,,,,, ,    ,, @@@@@@@,, @@@@@@@@@(
#                                                                  ,,,,,,,,,,  @,,,,,@@@@@@@@ ,,,,,
#                                                                   ,,,,,,,,  @ ,,,,&@@@@@@ ,,,,,,,
#                                                       ,,,,,,       ,,,, ,  @@@@ @@@@@@@@@ ,, ,,,
#                                                  ,,,,,,,,,,,,       , ,,, @@@@@@@@@@@@@@@@@ ,,,
#                                                ,,,,,,,,,,,,,,,,      , , @@@@@@@@@@@@@@@  ,,,
#                                               ,,,,,,,,,,,,,,,,,,,,,,, ,,,,@@@@@@@@@ ,,,,,,,,
#                                                ,,,,,,,,,,,,,,,,,,,,  ,,,.@@@@@@@@@    @ ,,
#                                                   ,,,,,,,,, ,,,    ,,,,,@@@@@.@@@@@@, ,,
#                                                              @@@@   .,,, ,,,,,,,,,,,,,
#                                                                 @@   ,,,,,,,,,,,,,,,
#
#
#
#
#  Autori:
#  ALEX CIACCIARELLA    N86003179
#  STEFANO DE FENZA    N86003446
#  ELVINO BUONANNO      N86003302
#  GUGLIELMO DE BIASIO     N86003216
#

# default imports
import logging
import signal
import socket
import time


# downloaded imports


# attributi globali
Port = 9091
IpAddr = "localhost"
s = socket.socket()
access_token = '0ffd6eb3150512'




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


        if CloseConnection():
            client.close()
            break




def CloseConnection():
    print("Do you Want To close the connection?")
    print("1)Yes")
    print("2)No")

    response = input()
    if response == "2":
        return False
    elif response == "1":
        return True
    else:
        return CloseConnection()




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
    else:
        return ConnectionMenu()


def main():
    esisteclient = False
    CreaSocket()
    CreaBind()
    while not esisteclient:
        client, _ = Listen()
        Operazioni(client)
        esisteclient = ConnectionMenu()
    s.close()



def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)

def Phantom():
    print("""                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                   ,,,,,,,,,,,                                                                        
                                                            ,,,,,,,,,,,,                                                                              
                                                       ,,,,,,,,,,,,, ,,,   ,                                                                          
                                                  ,,,,,,,,,,,,,,, ,, ,,,    ,                                                                         
                                               ,,,,,,,,,,,,,,,,,,,,, ,,,, , ,                                                                         
                                            ,,,,,,,,,,,,,,,,,,,,,,,,, ,,,   ,.                                                                        
                                           ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ,,,                                                                        
                                         ,,,,,,,,,,,,,   ,,,,,,,,,,,,, ,,,,  ,                                                                        
                                         ,,,,,,,,,         ,,,,,,,,,,,, ,,,  ,,                                                                       
                                                          , ,,,,,,,,,,,,.,,,  ,                                                                       
                                                           ,,,,,,,,,,,,,,,,,, ,,                        @                                             
                                                             , ,,,,,,,,,,,,,,           ,                                                             
                                                              , ,,,,,,,,,,, ,      ,,                      @@                                         
                                                                 ,,,,,,,,,,  ,, ,,        @@       ,     @                                            
                                                                  ,,,,,,, ,,,,,,      &@@   ,,,,,,,,   @@                                             
                                                                    ,, ,,,,,,,      @@@@ ,,,, @ ,,,  @@@                                              
                                                                   ,,,,,,, ,      @@@@@@,,,,@@ ,,,@@@@@                                               
                                                               ,,,,,,,,,, ,    ,, @@@@@@@,, @@@@@@@@@(                                                
                                                                ,,,,,,,,,,  @,,,,,@@@@@@@@ ,,,,,                                                      
                                                                 ,,,,,,,,  @ ,,,,&@@@@@@ ,,,,,,,                                                      
                                                     ,,,,,,       ,,,, ,  @@@@ @@@@@@@@@ ,, ,,,                                                       
                                                ,,,,,,,,,,,,       , ,,, @@@@@@@@@@@@@@@@@ ,,,                                                        
                                              ,,,,,,,,,,,,,,,,      , , @@@@@@@@@@@@@@@  ,,,                                                          
                                             ,,,,,,,,,,,,,,,,,,,,,,, ,,,,@@@@@@@@@ ,,,,,,,,                                                           
                                              ,,,,,,,,,,,,,,,,,,,,  ,,,.@@@@@@@@@    @ ,,                                                             
                                                 ,,,,,,,,, ,,,    ,,,,,@@@@@.@@@@@@, ,,                                                               
                                                            @@@@   .,,, ,,,,,,,,,,,,,                                                                 
                                                               @@   ,,,,,,,,,,,,,,,                                                                   
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      """)
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    Phantom()
    main()
