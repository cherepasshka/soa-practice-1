import socket
import os
import sys
from defaults import *


def handle_command(command_line: str, query: str, udp_sock: socket.socket, sender: tuple, serializers: dict[tuple]):
    command, method = command_line.split()
    if command == 'get_statistics':
        if method not in serializers.keys():
            udp_sock.sendto(f'Undefined serializer: {method}'.encode(), sender)
            return
        request = query + f'{SENDER_PREFIX}: {str(sender)}\n'
        udp_sock.sendto(request.encode(), serializers[method])
        udp_sock.sendto(
            f'{SERIALIZER_QUERY_ENDING}\n'.encode(), serializers[method])
    else:
        udp_sock.sendto(f'Undefined command: {command}'.encode(), sender)


def get_address(token):
    if '\n' in token:
        token = token[:token.index('\n')]
    address, port = token[1:-1].split(',')
    if '"' in address:
        address = address.replace('"', '')
    if "'" in address:
        address = address.replace("'", '')
    return (address, int(port))


def accept_connections(host: str, port: int, serializers: dict[tuple]):
    udp_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_sock.bind((host, port))
    recieved_data = dict()
    while True:
        message, address = udp_sock.recvfrom(1024)
        if address not in recieved_data.keys():
            recieved_data[address] = b''
        ending = f'{USER_QUERY_ENDING}\n'.encode()
        if ending in message:
            index = message.index(ending)
            recieved_data[address] += message[:index]
            if SENDER_PREFIX.encode() in recieved_data[address]:
                token = f'{SENDER_PREFIX}: '.encode()
                indx = recieved_data[address].index(token)
                sender_token = recieved_data[address][indx +
                                                      len(token):]
                info = recieved_data[address][:indx]
                sender = get_address(sender_token.decode())
                udp_sock.sendto(info, sender)
            else:
                recv_data = recieved_data[address]
                enter_index = recv_data.index(b'\n')
                command_line = recv_data[:enter_index].decode()
                query = recv_data[enter_index + 1:].decode()
                handle_command(command_line, query, udp_sock,
                               address, serializers)

            recieved_data[address] = message[index + len(ending):]
        else:
            recieved_data[address] += message


def get_serializers_addresses() -> dict[tuple]:
    serializers_formats = [
        'JSON',
        'MESSAGEPACK',
        'NATIVE',
        'YAML',
        'XML',
        'AVRO',
        'PROTO'
    ]
    serializers = {}
    for format in serializers_formats:
        if format in os.environ.keys():
            port = int(os.environ[format])
            serializer_server = format.lower() + '-server'
            serializers[format] = (serializer_server, port)
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
    serializers['all'] = (mcast_group, mcast_port)
    return serializers


if __name__ == '__main__':
    if 'HOST' in os.environ.keys():
        host = os.environ['HOST']
    else:
        host = LOCALHOST
    if 'PORT' in os.environ.keys():
        port = int(os.environ['PORT'])
    else:
        port = 2000
    serializers = get_serializers_addresses()
    print(serializers)
    try:
        accept_connections(host, port, serializers)
    except Exception as e:
        print('Error occured:', e)
