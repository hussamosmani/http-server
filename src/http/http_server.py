from src.http.processor import HTTPProcessor
from src.http.request_parser import HTTPParser
from src.core.tcp_server import TCPServer
from src.http.router import RouterTrie
from src.http.methods import HTTPMethod


class HTTPServer(TCPServer):

    def __init__(self):
        super().__init__()
        self.routes_trie = RouterTrie()
        self.http_parser = HTTPParser()
        self.http_processor = HTTPProcessor(router=self.routes_trie)

    def get(self, path):
        return self.route(path=path)(HTTPMethod.GET)

    def post(self, path):

        return self.route(path=path)(HTTPMethod.POST)

    def put(self, path):
        return self.route(path=path)(HTTPMethod.PUT)

    def route(self, path: str):
        def wrapper(method_type: HTTPMethod):
            def decorator(method):
                self.routes_trie.insert(
                    path=path, handler=method, method_type=method_type
                )

            return decorator

        return wrapper

    def handle_request(self, data: str):
        method_str, request_target, protocol, data = self.http_parser.parse_request(
            data=data
        )
        self.http_processor.handle_request(
            method_str=method_str, request_target=request_target, data=data
        )
