import selectors
import socket
import types
from base_automation import report


class MultiServer:

    def __init__(self, host='127.0.0.1', port=8080, buffer=2048):
        self._host = host
        self._port = port
        self._buffer = buffer
        self._server_socket = self.__create_server()
        self._selectors = selectors.DefaultSelector()

    @report.step('create server socket_connections')
    def __create_server(self):
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(e)
            assert False

    @report.step('accept wrapper')
    def accept_wrapper(self, sock):
        conn, address = sock.accept()  # Should be ready to read
        print('\n\naccepted connection from', address)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self._selectors.register(conn, events, data=data)

    @report.step('service connection')
    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            receive_data = sock.recv(self._buffer)  # Should be ready to read
            if receive_data:
                data.outb += receive_data
            else:
                print('closing connection to', data.addr)
                self._selectors.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('echoing', repr(data.outb), 'to', data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    @report.step('listen to client')
    def listen_to_client(self):
        print("Socket Started")
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        print('listening on', (self._host, self._port))
        self._server_socket.setblocking(False)
        self._selectors.register(self._server_socket, selectors.EVENT_READ, data=None)

        while True:
            events = self._selectors.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)

    @report.step('close server socket_connections')
    def close_socket(self):
        self._server_socket.close()
        print("server socket_connections closed")
