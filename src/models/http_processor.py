from typing import Any, Callable, Dict
from src.exceptions.http_exception import HTTPMethodException
from src.models.http_methods import HTTPMethod
from pydantic.main import ModelMetaclass
from src.models.router_trie import RouterTrie


class HTTPProcessor:

    def __init__(self, router: RouterTrie):
        self.router = router

    def handle_request(self, method_str: str, request_target: str, data: any = None):
        try:
            method = HTTPMethod(method_str)
        except ValueError:
            raise HTTPMethodException(method_str)
        body = body if method in {HTTPMethod.POST, HTTPMethod.PUT} else None
        self._handle_request(method=method, request_target=request_target, data=body)

    def _handle_request(
        self, method: HTTPMethod, request_target: str, data: any = None
    ):
        found_handler_and_args = self.router.search(
            path=request_target, method_type=method
        )
        if not found_handler_and_args:
            return
        handler, args = found_handler_and_args

        request = self._extract_pydantic_model(handler, data) if data else {}

        combined_args = {**args, **request} if data and request else args

        handler(**combined_args)

        exit()

    def _extract_pydantic_model(self, handler: Callable, data: dict) -> Dict[str, Any]:
        for param_name, annotation in handler.__annotations__.items():
            if isinstance(annotation, ModelMetaclass):
                return {param_name: annotation(**data)}
        return {}
