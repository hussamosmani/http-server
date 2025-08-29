import socket

from src.http.models.response import JSONResponse


class TCPServer:

    def __init__(self):
        res_list = socket.getaddrinfo(
            None, port=80, family=socket.AF_INET, type=socket.SOCK_STREAM
        )

        family, socktype, proto, canonname, sockaddr = res_list[0]

        s = socket.socket(family=family, type=socktype, proto=proto)

        s.bind(sockaddr)

        self.s = s

        self.s.listen(10)

    def run(self):
        while True:
            conn, client_addr = self.s.accept()
            try:
                data = conn.recv(1024)
                res = self.handle_request(data.decode())
                conn.sendall(bytes(res))
            finally:
                conn.close()

    def handle_request(self, data: str) -> JSONResponse:
        """This should be overridden by subclasses"""
        pass
