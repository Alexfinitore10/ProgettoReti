import json
import logging
import math
import os
import platform
import re
import shutil
import signal
import socket
import time
import uuid
from datetime import datetime
from typing import Tuple

import ipinfo
# imported Libraries
import psutil
from cpuinfo import get_cpu_info

access_token = ''
IpAddr = "localhost"
# IpAddr = "151.75.102.19"
Port = 41909
info = {}
s = socket.socket()

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
    elif req == '2': #CPU
        data = Cores()
        print(data)
        s.send(data)
        return True
    elif req == '3': #RAM
        data = ram()
        s.send(data)
        return True
    elif req == '4': #PARTITION
        data = Partizioni()
        s.send(data)
        return True
    elif req == '5': #NETWORK
        data = Network()
        s.send(data)
        return True
    elif req == '6': #GEOLOCATION
        data = Geolocation()
        s.send(data)
        return True
    else:
        print("exiting")
        return False

def Connection():
    global s
    connected = False
    while not connected:
        try:
            s.connect((IpAddr, Port))
            print("Socket successfully created and connected")
            connected = True
            token = s.recv(14).decode()
            return token
        except socket.error as se:
            print("Error connecting the socket. Trying again every 5s")
            time.sleep(5)

def main():
    global access_token
    resp = True
    CreaSocket()
    access_token = Connection()
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
            psutil.virtual_memory().total)  # str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB" #da aggiustare
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
        info['ip-address'] = details.ip#socket.gethostbyname(socket.gethostname())
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


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
