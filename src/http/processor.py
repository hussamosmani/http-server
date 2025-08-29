from typing import Any, Callable, Dict
from pydantic.main import ModelMetaclass

from src.http.models.response import JSONResponse
from src.exceptions.http_exception import HTTPMethodException
from src.http.models.methods import HTTPMethod
from src.http.models.headers import Headers
from src.http.router import RouterTrie


class HTTPProcessor:
    def __init__(self, router: RouterTrie):
        self.router = router

    def handle_request(
        self,
        method_str: str,
        request_target: str,
        headers: Headers,
        data: Any = None,
    ) -> JSONResponse:
        """
        Entry point: converts method string to enum, validates, and dispatches to handler.
        """
        try:
            method = HTTPMethod(method_str)
        except ValueError:
            raise HTTPMethodException(method_str)

        body = data if method in {HTTPMethod.POST, HTTPMethod.PUT} else None
        return self._dispatch_to_handler(method, request_target, headers, body)

    def _dispatch_to_handler(
        self, method: HTTPMethod, path: str, headers: Headers, body: Any = None
    ) -> JSONResponse:
        """
        Resolves the handler from the router and invokes it with parsed args.
        """
        match = self.router.search(path=path, method_type=method)
        if not match:
            return  # or raise NotFoundException

        handler, path_args = match
        model_args = self._build_model_args(handler, body) if body else {}

        headers = {"headers": headers} if "headers" in handler.__annotations__ else {}

        combined_args = {**path_args, **model_args, **headers}
        return handler(**combined_args)

    def _build_model_args(
        self, handler: Callable, body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parses request body into a Pydantic model, if applicable.
        """
        for param_name, annotation in handler.__annotations__.items():
            if isinstance(annotation, ModelMetaclass):
                return {param_name: annotation(**body)}
        return {}
