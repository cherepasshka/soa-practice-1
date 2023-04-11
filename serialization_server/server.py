import socket
import os
from serialization_module.serializer import create_serializer
from serialization_module.base_serializer import BaseSerializer
from formatted_data import parse_dict


def accept_connections(host: str, port: int, serializer: BaseSerializer):
    recieved_data = dict()
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((host, port))
    while True:
        try:
            message, address = udp_sock.recvfrom(1024)
        except KeyboardInterrupt:
            udp_sock.close()
            return
        if address not in recieved_data.keys():
            recieved_data[address] = b''
        ending = b'>>>'
        if ending in message:
            index = message.index(ending)
            recieved_data[address] += message[:index]
            data, sender = parse_dict(recieved_data[address].decode())
            info = serializer.get_info(data)
            responce = info + f'SENDER: {sender}\n'
            udp_sock.sendto(responce.encode(), address)
            udp_sock.sendto(b'end\n', address)
            recieved_data[address] = message[index + len(ending):]
        else:
            if not message.endswith(b'\n'):
                message += b'\n'
            recieved_data[address] += message


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
        host = '127.0.0.1'
    if 'PORT' in os.environ.keys():
        port = int(os.environ['PORT'])
    else:
        port = 65431
    serializer = create_serializer(method)
    try:
        accept_connections(host, port, serializer)
    except Exception as e:
        print('Error occured:', e)
