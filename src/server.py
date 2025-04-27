import socket


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

    def connect(self):
        conn, client_addr = self.s.accept()
        data = conn.recv(1024)
