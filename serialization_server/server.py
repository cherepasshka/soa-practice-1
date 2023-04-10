import socket
import os
from serialization_module.serializer import create_serializer
from serialization_module.base_serializer import BaseSerializer
from formatted_data import parse_dict


def accept_connections(host: str, port: int, serializer: BaseSerializer):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = ''
            while True:
                batches = conn.recv(1024).decode()
                lines = batches.split('\n')
                for batch in lines:
                    if '>>>' == batch[:3]:
                        student = parse_dict(data)
                        info = serializer.get_info(student)
                        conn.sendall(info.encode())
                        data = ''
                        break
                    data += batch + '\n'
                if not batches:
                    break


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
