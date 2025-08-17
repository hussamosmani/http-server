import json
from typing import Tuple, Dict
from src.http.models.methods import HTTPMethod
from urllib.parse import parse_qs

supported_headers = set(["Content-Type"])


class HTTPParser:
    def parse_request(self, raw_request: str) -> Tuple[str, str, str, Dict]:
        """
        Parses the raw HTTP request string into method, path, protocol, and body.
        """
        lines = raw_request.strip().split("\r\n")
        if not lines or len(lines[0].split(" ")) != 3:
            raise ValueError("Malformed request line")

        method, path, protocol = lines[0].split(" ")

        headers_list = lines[1:-2]
        for header in headers_list:
            header_name, header_value = header.split(":")
            header_name, header_value = header_name.strip(), header_value.strip()
            if header_name not in supported_headers:
                exit()
            if header_name == "Content-Type":
                if header_value == "application/json":
                    try:
                        body = json.loads(lines[-1])
                    except json.JSONDecodeError:
                        raise ValueError("Invalid JSON body")
                elif header_value == "application/x-www-form-urlencoded":
                    parsed = parse_qs(lines[-1])
                    body = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

                else:
                    exit()

        return method, path, protocol, body
