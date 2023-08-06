import socket
from base_automation import report


class ClientSocket:

    def __init__(self, host='127.0.0.1', port=8080, buffer=2048):
        self._host = host
        self._port = port
        self._buffer = buffer
        self._client_socket = self.__connect_to_server()

    @report.step('create server socket_connections')
    def __connect_to_server(self):
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(e)
            assert False

    @report.step('send message to server')
    def send_message(self, messages: list):
        self._client_socket.connect((self._host, self._port))
        for x in messages:
            self._client_socket.sendall(x)
            data = self._client_socket.recv(self._buffer)
            print('Received', repr(data))

    @report.step('close socket_connections')
    def close_socket(self):
        self._client_socket.close()
        print("client socket_connections closed")
