import socket
from base_automation import report


class ServerSocket:

    def __init__(self, host='127.0.0.1', port=8080, buffer=2048):
        self._host = host
        self._port = port
        self._buffer = buffer
        self._data = None
        self._server_socket = self.__create_server()

    @report.utils.step('create server socket_connections')
    def __create_server(self):
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(e)
            assert False

    @report.utils.step('listen to client')
    def listen_to_client(self):
        print("Socket Started")
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        print('listening on', (self._host, self._port))
        conn, address = self._server_socket.accept()
        with conn:
            print('Connected by', address)
            while True:
                self._data = conn.recv(self._buffer)
                if not self._data:
                    break

                conn.sendall(self._data)
                print(self._data)

    @report.utils.step('close server socket_connections')
    def close_socket(self):
        self._server_socket.close()
        print("server socket_connections closed")

    @report.utils.step('str to bytes')
    def __str_to_bytes(self):
        self._data = str.encode(self._data)
        print(type(self._data))  # ensure it is byte representation
