# JSONResponse
from typing import Dict
import json
from src.http.models.headers import Headers, SupportedHeaders


class JSONResponse:
    def __init__(self, content: Dict[str, str], custom_headers: Dict[str, str] = None):
        self._content = content
        self._headers: Dict[str, str] = {}
        if custom_headers:
            self._headers.update(custom_headers)

    def add_required_headers(self, headers: Headers):
        # Make sure keys are strings, not enum objects
        self._headers[SupportedHeaders.CONTENT_TYPE.value] = headers.get(
            SupportedHeaders.CONTENT_TYPE
        )
        body_str = json.dumps(self._content)
        self._headers[SupportedHeaders.CONTENT_LENGTH.value] = str(
            len(body_str.encode("utf-8"))
        )

    def __str__(self):
        headers_str = "\n".join(f"{k}: {v}" for k, v in self._headers.items())
        body_str = json.dumps(self._content)
        return f"{headers_str}\n\n{body_str}"

    # NEW: bytes encoder
    def to_bytes(self) -> bytes:
        body_bytes = json.dumps(self._content).encode("utf-8")

        self._headers.setdefault(
            SupportedHeaders.CONTENT_TYPE.value,
            self._headers[SupportedHeaders.CONTENT_TYPE.value],
        )
        self._headers[SupportedHeaders.CONTENT_LENGTH.value] = str(len(body_bytes))

        headers_block = (
            "\r\n".join(
                f"{(k.value if hasattr(k, 'value') else k)}: {v}"
                for k, v in self._headers.items()
            )
            + "\r\n\r\n"
        )

        return headers_block.encode("iso-8859-1") + body_bytes

    def __bytes__(self) -> bytes:
        return self.to_bytes()
