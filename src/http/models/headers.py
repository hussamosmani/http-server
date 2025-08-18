from typing import Dict


class Headers:

    def __init__(self, headers_dict: Dict[str, str]):
        self._headers_dict = headers_dict

    def get(self, header_key: str):
        return self._headers_dict[header_key]

    def __str__(self):
        return str(self._headers_dict)
