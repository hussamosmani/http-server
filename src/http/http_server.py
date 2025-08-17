from src.http.processor import HTTPProcessor
from src.http.request_parser import HTTPParser
from src.core.tcp_server import TCPServer
from src.http.router import RouterTrie
from src.http.models.methods import HTTPMethod
from typing import Callable


class HTTPServer(TCPServer):
    def __init__(self):
        super().__init__()
        self.routes_trie = RouterTrie()
        self.http_parser = HTTPParser()
        self.http_processor = HTTPProcessor(router=self.routes_trie)

    def get(self, path: str):
        return self._register_route(path, HTTPMethod.GET)

    def post(self, path: str):
        return self._register_route(path, HTTPMethod.POST)

    def put(self, path: str):
        return self._register_route(path, HTTPMethod.PUT)

    def _register_route(self, path: str, method: HTTPMethod):
        def decorator(func: Callable):
            self.routes_trie.insert(path=path, handler=func, method_type=method)

        return decorator

    def handle_request(self, raw_data: str):
        method_name, request_target, protocol, body = self.http_parser.parse_request(
            raw_data
        )
        self.http_processor.handle_request(
            method_str=method_name, request_target=request_target, data=body
        )
        exit()
