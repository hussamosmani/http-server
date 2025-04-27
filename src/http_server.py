from enum import Enum
from src.exceptions.http_exception import HTTPMethodException
from src.tcp_server import TCPServer


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


class HTTPServer(TCPServer):

    def __init__(self):
        super().__init__()

    def handle_request(self, data: str):
        method, request_target, protocol = data.split()
        print(method, request_target, protocol)
        if method == HTTPMethod.GET:
            pass
        elif method == HTTPMethod.POST:
            pass
        elif method == HTTPMethod.PUT:
            pass
        else:
            raise HTTPMethodException(method)
