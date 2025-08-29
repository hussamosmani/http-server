from enum import Enum
from typing import Dict


class Headers:

    def __init__(self, headers_dict: Dict[str, str]):
        self._headers_dict = headers_dict

    def get(self, header_key: str):
        return self._headers_dict[header_key]

    def __str__(self):
        return str(self._headers_dict)


class SupportedHeaders(str, Enum):
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"
    ACCEPT = "Accept"
    AUTHORIZATION = "Authorization"  # prefer US spelling
    USER_AGENT = "User-Agent"
    CACHE_CONTROL = "Cache-Control"
    ACCEPT_ENCODING = "Accept-Encoding"
