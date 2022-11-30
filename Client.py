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

# imported Libraries
import ipinfo
import psutil
from cpuinfo import get_cpu_info

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


''' while not connected:
    try:
        #s.connect((IpAddr, Port))
        print("Socket successfully created and connected")
        token = s.recv(14).decode()
        return token
    except socket.error as se:
        print("Error connecting the socket. Trying again every 5s")
        time.sleep(5)'''


def main():
    global access_token
    resp = True
    CreaSocket()
    mainThreadingFunction()
    access_token = getTokenFromConnection()
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


def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    s.close()
    exit(0)


#  --------------------------------THREADING AND IP CHECKING FUNCTIONS--------------------------------------------------


def mainThreadingFunction():
    print("Scannerizzo gli ip della sottorete per trovare quello del server...")
    ricerca = False
    threads = []
    number_of_threads = 50
    list1 = []

    list1 = splitter(number_of_threads)

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
        if Connesso == True and checkConnection(i):
            print(f"Sono riuscito a connettermi a {i} ")
            IpAddr = str(i)
            retry = False
            return retry
        elif Connesso == False:
            pass
        else:
            print(f"Non sono riuscito a connettermi a {i} ")
    return retry

def checkConnection(i):
    global s
    print(f"Mi provo a connettere a {i}")
    try:
        s = socket.create_connection((socket.gethostbyname(str(i)), 9091))
        if s:  # sock.connect_ex((socket.gethostbyname(str(i)), 9091)) == 0:
            return True
        else:
            return False
    except socket.error as e:
        return False


def splitter(passo):
    numberlist = []
    for i in range(2, 255):
        numberlist.append(f"192.168.1.{i}")
    return numberlist

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
