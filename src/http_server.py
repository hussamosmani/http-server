import inspect
import json

from pydantic.main import ModelMetaclass
from src.exceptions.http_exception import HTTPMethodException
from src.tcp_server import TCPServer
from src.models.router_trie import RouterTrie
from src.models.http_methods import HTTPMethod


class HTTPServer(TCPServer):

    def __init__(self):
        super().__init__()
        self.routes_trie = RouterTrie()

    def get(self, path):

        def wrapper(method):
            self.routes_trie.insert(
                path=path, handler=method, method_type=HTTPMethod.GET.value
            )

        return wrapper

    def handle_request(self, data: str):
        request = data.split("\r\n")
        method, request_target, protocol = request[0].split(" ")
        data = json.loads(request[2]) if len(request) > 2 else None
        if method == HTTPMethod.GET.value:
            self._handle_request(request_target=request_target)

        elif method == HTTPMethod.POST.value:
            self._handle_request(request_target=request_target, data=data)

        elif method == HTTPMethod.PUT.value:
            pass
        else:
            raise HTTPMethodException(method)

    def _handle_request(self, request_target: str, data: any = None):
        found_handler_and_args = self.routes_trie.search(
            path=request_target, method_type=HTTPMethod.GET
        )
        if not found_handler_and_args:
            return
        handler, args = found_handler_and_args

        request = None
        for parameter, annotation in handler.__annotations__.items():
            if isinstance(annotation, ModelMetaclass):
                request = {parameter: annotation(**data)}

        combined_args = {**args, **request} if data and request else args

        handler(**combined_args)

        exit()
