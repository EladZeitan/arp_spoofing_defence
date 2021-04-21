from util.UtilConstants import UtilConstants
from Constants import ClientConstants
from scapy.all import *
import socket
import threading
from getmac import get_mac_address
import subprocess
import time
import os


def get_router_ip():
    output = subprocess.check_output("ipconfig")
    gateway_index = output.find('Gateway'.encode())
    output = output[gateway_index:-1]
    output = output.split(' : '.encode())
    output = output[1].split('\r\n'.encode())
    output = output[0].decode()
    return output


def get_ip():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return ip


def handle_message(data):
    print('DATA: ' + data)
    data = data.split(UtilConstants.DATA_SEPARATOR)
    message_type = data[0]
    if message_type == 'WARN':
        t = threading.Thread(target=kill_virus)
        t.start()

    if message_type == 'ALERT' or message_type == 'WARN':
        data.pop(0)
        update_data_base(data)


def send_data(local_socket: socket.socket, data: str):
    to_send = data + UtilConstants.MESSAGE_END
    local_socket.send(to_send.encode())


def receive_data(local_socket: socket.socket):
    data = local_socket.recv(1).decode()
    if len(data) > 0:
        while data[-1] != '$':
            data += local_socket.recv(1).decode()

    return data[0:-1]


def receive_id(local_socket: socket.socket):
    data = receive_data(local_socket)
    # format ID!group!client_id
    data = data.split(UtilConstants.DATA_SEPARATOR)
    if data[0] == 'ID':
        ClientConstants.ID = (data[1], data[2])


def kill_virus():
    dir_content = os.listdir()
    for item in dir_content:
        if os.path.isdir(item):
            os.chdir(item)
            kill_virus()

    output = (subprocess.check_output('attrib')).decode()
    output = output.split('\r\n')
    for line in output:
        if 'S' or 'H' or 'R' in file:
            file = line.split('\\')[-1]
            ending = file.split('.')[-1]
            if ending == 'inf' or ending == 'exe':
                subprocess.check_output('attrib -s -h -r -a -i {}'.format(file))
                subprocess.check_output('del {}'.format(file))

    if os.getcwd() != 'c:\\':
        os.chdir('../')
        return


def report(local_socket: socket.socket):

    to_send = ClientConstants.REPORT_MESSAGE.format(ClientConstants.ATTACKER_MAC_ADDRESS)
    send_data(local_socket, to_send)

    # send_data(local_socket, ClientConstants.REPORT_MESSAGE.format(ClientConstants.ATTACKER_MAC_ADDRESS,
    #           ClientConstants.ID[0], ClientConstants.ID[1]))


def update_cache():
    proc = subprocess.check_output("arp -a")
    proc = proc.split('\r\n'.encode())[3:-1]
    for i in proc:
        line = i.decode()
        line = line.split(' ')
        line = list(dict.fromkeys(line))
        ClientConstants.CACHE[line[1]] = line[2]


def update_data_base(data: list):
    print('ADD ATTACK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    ClientConstants.ATTACKS_DATA.add_row([data[0], data[1]])


def filter_arp(packet_to_check):
    return ARP in packet_to_check and packet_to_check[ARP].op == 2


def block_attack():
    victim_ip = get_ip()
    send(ARP(op=2, pdst=ClientConstants.ROUTER_IP, psrc=victim_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=get_mac_address()))
    send(ARP(op=2, pdst=victim_ip, psrc=ClientConstants.ROUTER_IP,
             hwdst="ff:ff:ff:ff:ff:ff", hwsrc=ClientConstants.CACHE[ClientConstants.ROUTER_IP]))


def scan(local_socket: socket.socket):

    while True:
        packet_to_check = sniff(count=1, store=1, lfilter=filter_arp)
        source_ip = packet_to_check[0].psrc
        source_mac = packet_to_check[0].hwsrc
        source_mac = source_mac.replace(':', '-')
        print(ClientConstants.CACHE)

        if source_ip in ClientConstants.CACHE and ClientConstants.CACHE[source_ip] != source_mac:
            print('FOUND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('source_ip: {}     source_mac: {}'.format(source_ip, source_mac))
            ClientConstants.FOUND_ATTACK = True
            ClientConstants.ATTACKER_MAC_ADDRESS = source_mac
            report(local_socket)
            block_attack()
        else:
            ClientConstants.CACHE[source_ip] = source_mac


def manage(local_socket: socket.socket):

    data = ''
    # thread
#   gui_thread = threading.Thread(target=start_gui)
#    gui_thread.start()

    t = threading.Thread(target=scan, args=(local_socket,))
    t.start()

    while True:
        data = receive_data(local_socket)
        print('ALERT@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        handle_message(data)


def main():

    UtilConstants.DATA_BASES_PATH = os.getcwd() + '\\DataBases'

    ClientConstants.ROUTER_IP = get_router_ip()
    mac_address = get_mac_address().replace(':', '-')

    update_cache()

    ClientConstants.SOCKET_ADDRESS = (get_ip(), ClientConstants.PORT)

    local_socket = socket.socket()
    local_socket.connect(ClientConstants.SOCKET_ADDRESS)
    send_data(local_socket, ClientConstants.SIGN_UP_MESSAGE.format(ClientConstants.ROUTER_IP, mac_address))

    confirm = receive_data(local_socket)
    # receive_id(local_socket)

    manage(local_socket)


if __name__ == '__main__':
    main()
