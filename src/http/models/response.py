from typing import Dict
import json

from src.http.models.headers import Headers, SupportedHeaders


class JSONResponse:

    def __init__(self, content: Dict[str, str], custom_headers: Dict[str, str] = None):
        self._content = content
        self._headers = {}
        if custom_headers:
            self._headers.update(custom_headers)

    def add_required_headers(self, headers: Headers):
        self._headers[SupportedHeaders.CONTENT_TYPE] = headers.get(
            SupportedHeaders.CONTENT_TYPE
        )

        body_str = json.dumps(self._content)
        self._headers[SupportedHeaders.CONTENT_LENGTH] = str(
            len(body_str.encode("utf-8"))
        )

    def __str__(self):
        headers_str = "\n".join(f"{k}: {v}" for k, v in self._headers.items())
        body_str = json.dumps(self._content)
        return f"{headers_str}\n\n{body_str}"
