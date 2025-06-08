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
            pass
        elif method == HTTPMethod.POST.value:
            pass
        elif method == HTTPMethod.PUT.value:
            pass
        else:
            raise HTTPMethodException(method)
