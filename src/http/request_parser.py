import json
from typing import Tuple, Dict
from src.http.models.headers import Headers, SupportedHeaders
from urllib.parse import parse_qs
from enum import Enum


class HTTPParser:
    def parse_request(self, raw_request: str) -> Tuple[str, str, str, Dict, Headers]:
        """
        Parses the raw HTTP request string into method, path, protocol, and body.
        """
        lines = raw_request.strip().split("\r\n")
        if not lines or len(lines[0].split(" ")) != 3:
            raise ValueError("Malformed request line")

        method, path, protocol = lines[0].split(" ")

        headers_list = lines[1:-2]
        headers_dict: Dict[str, str] = {}
        body: Dict = {}

        for header in headers_list:
            if ":" not in header:
                raise ValueError(f"Malformed header line: {header}")

            header_name, header_value = header.split(":", 1)
            header_name, header_value = header_name.strip(), header_value.strip()
            headers_dict[header_name] = header_value

            # validate against enum values
            if header_name not in [h.value for h in SupportedHeaders]:
                raise ValueError(f"Unsupported header: {header_name}")

            if header_name == SupportedHeaders.CONTENT_TYPE.value:
                if header_value == "application/json":
                    try:
                        body = json.loads(lines[-1])
                    except json.JSONDecodeError:
                        raise ValueError("Invalid JSON body")
                elif header_value == "application/x-www-form-urlencoded":
                    parsed = parse_qs(lines[-1])
                    body = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
                else:
                    raise ValueError(f"Unsupported Content-Type: {header_value}")

            elif header_name == SupportedHeaders.CONTENT_LENGTH.value:
                try:
                    content_length = int(header_value)
                except ValueError:
                    raise ValueError("Invalid Content-Length header (not an integer)")
                actual_length = len(lines[-1].encode())
                if actual_length != content_length:
                    raise ValueError(
                        f"Content-Length mismatch: expected {content_length}, got {actual_length}"
                    )

        headers = Headers(headers_dict)
        return method, path, protocol, body, headers
