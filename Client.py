import json
import logging
import re
import socket
import os
import sys
import time
import platform
import uuid
from datetime import datetime

# imported Libraries
import psutil
from mutagen._util import get_size

IpAddr = "127.0.0.1"
Port = 12000
info = {}


def AnalizyingReq(req):
    match req:
        case "1":
            return 1
        case _:
            pass


def CreazioneSocket():
    try:
        informazioni = {}  # Creo Un dizionario per immagazzinare informazioni

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket Created
        print("Socket Created")

        while True:
            s.connect((IpAddr, Port)) # connecting the socket to the Server
            print("Socket successfully created and connected")


            data = GetGeneralInfo()

            #s.send(f"Client Connected".encode())  # message sent

            # ora dobbiamo preoccuparci di Ottenere tutte le informazioni del dispositivo su cui runna questo
            # script.

            # Quindi il client deve essere silente finchè il server invia richieste

            req = s.recv(1024).decode()

            response = AnalizyingReq(req)

            if response == 1:
                s.send(data)
                s.close()
            else:
                pass



            time.sleep(5)




    except socket.error as se:
        print(f"Error creating the Socket")
        print("What do you want to do now?")
        print("1)Retry")
        print("2)Exit")
        resp = input()
        if resp == "1":
            pass
        elif resp == "2":
            exit()
        else:
            print("Rewrite the response better...")
            time.sleep(2)
            cls()


def main():
    CreazioneSocket()


def GetGeneralInfo():
    try:
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        info['Boot time'] = str(f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        info['Physical Cores'] = psutil.cpu_count(logical=False)
        info['Total Cores'] = psutil.cpu_count(logical=True)
        cpufreq = psutil.cpu_freq()
        info['Cpu Current Frequency'] = str(f"{cpufreq.current:.2f}Mhz")
        info['Cpu Max Frequency'] = str(f"{cpufreq.max:.2f}Mhz")
        info['Cpu Min Frequency'] = str(f"{cpufreq.min:.2f}Mhz")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            info[f'Cpu {i} Usage Per Core'] = str(f"Core {i}: {percentage}%")
        info['Total Cpu Usage'] = str(f"{psutil.cpu_percent()}%")
        swap = psutil.swap_memory()
        info['Total Swap Memory'] = str(sys.getsizeof(swap.total))
        info['Free Swap Memory'] = str(sys.getsizeof(swap.free))
        info['Used Swap Memory'] = str(sys.getsizeof(swap.used))
        info['Percentage Swap Memory Used'] = str(f"Total: {swap.percent}")
        partitions = psutil.disk_partitions()
        counter = 0
        for partition in partitions:
            info[f'Partition {counter}'] = str(partition.device)
            info[f'Mountpoint'] = str(partition.mountpoint)
            info['File System Type'] = str(partition.fstype)
            partition_usage = psutil.disk_usage(partition.mountpoint)
            info[f'Partition {counter} Total Size'] = str(sys.getsizeof(partition_usage.total))
            info[f'Partition {counter} Used'] = str(sys.getsizeof(partition_usage.used))
            info[f'Partition {counter} Free'] = str(sys.getsizeof(partition_usage.free))
            info[f'Partition {counter} Percentage'] = str(sys.getsizeof(partition_usage.percent))
            counter+=1
        disk_io = psutil.disk_io_counters()
        info['Total Read Since Boot'] = str(disk_io.read_bytes)
        info['Total Write Since Boot'] = str(disk_io.write_bytes)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    info[f'Interface {interface_name} Ip Address'] = address.address
                    info[f'Interface {interface_name} NetMask'] = address.netmask
                    info[f'Interface {interface_name} Broadcast IP'] = address.broadcast
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    info[f'Interface {interface_name} MAC Address'] = address.address
                    info[f'Interface {interface_name} NetMask'] = address.netmask
                    info[f'Interface {interface_name} Broadcast MAC'] = address.broadcast
        net_io = psutil.net_io_counters()
        info['Total Bytes Sent Since Launch'] = str(sys.getsizeof(net_io.bytes_sent))
        info['Total Bytes Received Since Launch'] = str(sys.getsizeof(net_io.bytes_recv))
        return json.dumps(info,indent=4).encode("utf-8")
    except Exception as e:
        logging.exception(e)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()
