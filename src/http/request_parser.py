import json
from typing import Tuple

from src.http.methods import HTTPMethod


class HTTPParser:

    def parse_request(self, data: str) -> Tuple[HTTPMethod, str, dict]:
        request = data.split("\r\n")
        method, request_target, protocol = request[0].split(" ")
        data = json.loads(request[2]) if len(request) > 2 else None
        return method, request_target, protocol, data
