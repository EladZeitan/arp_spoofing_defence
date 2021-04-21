from util.UtilConstants import UtilConstants
from Constants import ServerConstants
import telnetlib
import socket
import threading
from datetime import datetime


def send_data(client_socket: socket.socket, data: str):
    to_send = data + UtilConstants.MESSAGE_END
    client_socket.send(to_send.encode())


def receive_data(client_socket: socket.socket):
    data = client_socket.recv(1).decode()
    if len(data) > 0:
        while data[-1] != '$':
            data += client_socket.recv(1).decode()

    return data[0:-1]


def sign_in_client(client_socket: socket.socket, client_ip):

    data = receive_data(client_socket)
    data = data.split(UtilConstants.DATA_SEPARATOR)

    if data[0] == 'NEW':
        router_ip = data[1]
        client_mac = data[2]
        # group_clients = CLIENTS_DATA.select('router_ip', router_ip)
        # client_id = group_clients[-1][1] + 1
        # group_id = group_clients[-1][0]
        # CLIENTS_DATA.add_row([group_id, client_id, router_ip, client_ip, 0])
        ServerConstants.CLIENTS_DATA.add_row([router_ip, client_ip, client_mac, 0])
        # to_send = CLIENT_ID_MESSAGE.format(group_id, client_id)
        to_send = ServerConstants.REGISTRATION_COMPLETE_MESSAGE
        send_data(client_socket, to_send)


def update_client_attack(router_ip, attacker_mac):
    fetch = ServerConstants.CLIENTS_DATA.select('router_ip', router_ip)
    attacker_in_clients = False
    for i in fetch:
        print('UPDATING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(i[1])
        ServerConstants.CLIENTS_DATA.update(('is_attacked', 1), ('client_ip', i[1]))
        if i[2] == attacker_mac:
            attacker_in_clients = True

    if not attacker_in_clients:
        block_attacker(attacker_mac)


def update_attack(client_ip, attacker_mac):
    fetch = ServerConstants.CLIENTS_DATA.select('client_ip', client_ip)
    router_ip = fetch[0][0]
    data = get_date()
    ServerConstants.ATTACK_DATA.add_row([router_ip, data, attacker_mac])

    update_client_attack(router_ip, attacker_mac)


def get_date():
    data = datetime.now()
    data = data.strftime("%m/%d/%Y, %H:%M:%S")
    return data


def alert_client(client_socket: socket.socket, client_ip):

    while True:
        # get data on client from CLIENT DATA via client ip
        fetch = ServerConstants.CLIENTS_DATA.select('client_ip', client_ip)
        is_attack = fetch[0][3]
        if is_attack == 1:
            router_ip = fetch[0][0]
            client_mac = fetch[0][2]

            # get attack details from ATTACK DATA via router ip
            attack_details = ServerConstants.ATTACK_DATA.select('router_ip', router_ip)
            attack_date = attack_details[-1][1]
            attacker_mac = attack_details[-1][2]

            to_send = ''
            if client_mac == attacker_mac:
                client_attacks = ServerConstants.ATTACK_DATA.select('attacker_mac', client_mac)
                if len(client_attacks) > 5:
                    to_send = ServerConstants.BLOCK_MESSAGE
                    block_attacker(attacker_mac)

                else:
                    to_send = ServerConstants.WARNING_MESSAGE.format(attacker_mac, attack_date)
            else:
                to_send = ServerConstants.ALERT_MESSAGE.format(attacker_mac, attack_date)

            print('ALERT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(to_send)
            send_data(client_socket, to_send)
            ServerConstants.CLIENTS_DATA.update(('is_attacked', 0), ('client_ip', client_ip))


def block_attacker(attacker_mac):
    pass


def handle_connection(client_socket: socket.socket, client_ip):
    sign_in_client(client_socket, client_ip)
    t = threading.Thread(target=alert_client, args=(client_socket, client_ip))
    t.start()
    data = ''
    while True:
        data = receive_data(client_socket)
        data = data.split(UtilConstants.DATA_SEPARATOR)
        if data[0] == 'REP':
            print('REPORT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            attacker_mac = data[1]
            update_attack(client_ip, attacker_mac)


def main():
    server_socket = socket.socket()
    server_socket.bind(ServerConstants.ADDRESS)

    while True:
        server_socket.listen(1)
        client_socket, client_ip = server_socket.accept()
        client_ip = client_ip[0]
        t = threading.Thread(target=handle_connection, args=(client_socket, client_ip))
        t.start()


if __name__ == '__main__':
    main()
