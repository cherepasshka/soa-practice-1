import socket
import _thread
import os


def read_message(clientsocket: socket.socket) -> str:
    msg = clientsocket.recv(1024)
    return msg


def handle_command(line: list, serializers: dict[socket.socket], clientsocket: socket.socket) -> str:
    command = line[0]
    if command == 'help':
        with open('greeting_instruction.txt', 'r') as f:
            instruction = f.read()
        return instruction
    elif command == 'get_statistics':
        msg = read_message(clientsocket)
        method = line[1]
        serializers[method].send(msg)
        serializers[method].send(b'>>>')
        return serializers[method].recv(1024).decode()
    elif command == 'show_data_format':
        pass
    else:
        raise NameError('Unknown command', command)


def accept_new_client(clientsocket: socket.socket, serializers: dict[socket.socket]):
    instruction = ''
    with open('greeting_instruction.txt', 'rb') as f:
        instruction = f.read()
    with clientsocket:
        clientsocket.send(instruction)
        while True:
            msg = clientsocket.recv(1024)
            if not msg:
                break
            line = msg.decode().split()
            try:
                result = handle_command(line, serializers, clientsocket)
                clientsocket.send(result.encode())
            except NameError as e:
                clientsocket.send(str(e).encode())


def accept_connections(host: str, port: int, serializers: dict[socket.socket]):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            connection, addr = s.accept()
            _thread.start_new_thread(
                accept_new_client, (connection, serializers))


def connect_to_serializers() -> dict[socket.socket]:
    serializers_formats = [
        'JSON',
        'MESSAGEPACK',
    ]
    serializers = {}
    for format in serializers_formats:
        if format in os.environ.keys():
            port = int(os.environ[format])
            serializers[format] = socket.socket()
            serializer_server = format.lower() + '-server'
            serializers[format].connect((serializer_server, port))
    return serializers


if __name__ == '__main__':
    if 'HOST' in os.environ.keys():
        host = os.environ['HOST']
    else:
        host = '127.0.0.1'
    if 'PORT' in os.environ.keys():
        port = int(os.environ['PORT'])
    else:
        port = 2000
    serializers = connect_to_serializers()

    try:
        accept_connections(host, port, serializers)
    except Exception as e:
        print('Error occured:', e)
    finally:
        for format in serializers.keys():
            serializers[format].close()
