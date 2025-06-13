import json
from typing import Tuple, Dict
from src.http.methods import HTTPMethod


class HTTPParser:
    def parse_request(self, raw_request: str) -> Tuple[str, str, str, Dict]:
        """
        Parses the raw HTTP request string into method, path, protocol, and body.
        """
        lines = raw_request.strip().split("\r\n")
        if not lines or len(lines[0].split(" ")) != 3:
            raise ValueError("Malformed request line")

        method, path, protocol = lines[0].split(" ")

        try:
            body = json.loads(lines[2]) if len(lines) > 2 else {}
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body")

        return method, path, protocol, body
