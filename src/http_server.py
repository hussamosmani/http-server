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
        method, request_target, protocol = data.split()
        if method == HTTPMethod.GET.value:
            self._handle_get(request_target=request_target)

        elif method == HTTPMethod.POST.value:
            pass
        elif method == HTTPMethod.PUT.value:
            pass
        else:
            raise HTTPMethodException(method)

    def _handle_get(self, request_target: str):
        found_handler_and_args = self.routes_trie.search(
            path=request_target, method_type=HTTPMethod.GET
        )
        if not found_handler_and_args:
            return
        handler, args = found_handler_and_args

        handler(**args)

        exit()
