import socket
import os
import threading
import struct
import sys
from serialization_module.serializer import create_serializer
from serialization_module.base_serializer import BaseSerializer
from formatted_data import parse_dict
from defaults import *


def accept_connections(udp_sock: socket.socket, serializer: BaseSerializer):
    recieved_data = dict()
    while True:
        try:
            message, address = udp_sock.recvfrom(1024)
        except KeyboardInterrupt:
            udp_sock.close()
            return
        if address not in recieved_data.keys():
            recieved_data[address] = b''
        if SERIALIZER_QUERY_ENDING.encode() in message:
            index = message.index(SERIALIZER_QUERY_ENDING.encode())
            recieved_data[address] += message[:index]
            try:
                data, sender = parse_dict(recieved_data[address].decode())
                info = serializer.get_info(data)
                responce = info + f'{SENDER_PREFIX}: {sender}\n'
                udp_sock.sendto(responce.encode(), address)
                udp_sock.sendto(f'{USER_QUERY_ENDING}\n'.encode(), address)
            except Exception as e:
                print(e, file=sys.stderr)
            recieved_data[address] = message[index +
                                             len(SERIALIZER_QUERY_ENDING.encode()):]
        else:
            if not message.endswith(b'\n'):
                message += b'\n'
            recieved_data[address] += message


def create_udp_socket(host: str, port: int):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((host, port))
    return udp_sock


def create_mcast_udp_socket(multicast_group: str, multicast_port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', multicast_port))
    mreq = struct.pack("4sl", socket.inet_aton(
        multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


if __name__ == '__main__':
    method = None
    if 'METHOD' in os.environ.keys():
        method = os.environ['METHOD']
    else:
        print('Specify serialization method via $METHOD env variable')
        exit(1)

    if 'HOST' in os.environ.keys():
        host = os.environ['HOST']
    else:
        host = LOCALHOST
    if 'PORT' in os.environ.keys():
        port = int(os.environ['PORT'])
    else:
        port = 65431

    if 'MCAST_IP' in os.environ.keys():
        mcast_group = os.environ['MCAST_IP']
    else:
        mcast_group = LOCALHOST  # invalid ip range for multicast
        print(
            'Warning: $MCAST_IP was not set, so multicast will be disabled', file=sys.stderr)
    if 'MCAST_PORT' in os.environ.keys():
        mcast_port = int(os.environ['MCAST_PORT'])
    else:
        mcast_port = 65432
    serializer = create_serializer(method)
    try:
        mcast_udp_socket = create_mcast_udp_socket(mcast_group, mcast_port)
        threading.Thread(target=accept_connections, args=(
            mcast_udp_socket, serializer), daemon=True).start()
        accept_connections(create_udp_socket(host, port), serializer)
    except Exception as e:
        print('Error occured:', e)
