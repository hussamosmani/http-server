# HTTP Router Library — README

A tiny, explicit HTTP server + router built from sockets, a trie-based router, a request parser, a simple processor, and a JSON response helper. It’s designed to make declaring routes and handlers dead simple, including dynamic path params and Pydantic-powered request bodies.

---

## Features at a glance

- **Routing with a Trie**: Static paths and `{param}` segments (e.g. `/users/{id}`).
- **Decorators per method**: `@server.get`, `@server.post`, `@server.put`.
- **Typed bodies via Pydantic**: Declare a `BaseModel`-typed parameter in your handler and it’s auto-parsed.
- **Headers injection (opt-in)**: Include a `headers: Headers` parameter to receive request headers.
- **Bare-metal I/O**: Minimal TCP loop; sends back a JSON payload with headers.

> ⚠️ This is an educational/experimental stack. It’s synchronous, binds to port 80 by default, and omits many production HTTP features. See **Known limitations** below.

---

## Project layout

```
src/
  core/tcp_server.py         # TCPServer base (accept loop)
  http/http_server.py        # HTTPServer (route registration + request handling)
  http/request_parser.py     # HTTPParser (request line, headers, body)
  http/processor.py          # HTTPProcessor (dispatch to route handler)
  http/router.py             # RouterTrie + nodes
  http/models/
    methods.py               # HTTPMethod enum
    headers.py               # Headers wrapper + SupportedHeaders enum
    response.py              # JSONResponse
```

---

## Installation

Requires Python 3.10+.

```bash
pip install pydantic
# Your package/install steps here if you publish it,
# otherwise run directly from your project.
```

---

## Quick start

```python
from pydantic import BaseModel
from src.http.http_server import HTTPServer
from src.http.models.response import JSONResponse

server = HTTPServer()

@server.get("/health")
def health():
    return JSONResponse({"ok": True})

class User(BaseModel):
    user: str
    age: int

@server.post("/users/{user_id}")
def create_user(user_id: str, user: User):
    # path param + Pydantic body already parsed
    return JSONResponse({"created": user.user, "id": user_id})

print("Server listening…")
server.run()
```

---

## Authoring APIs

### 1) Register routes

Use the decorators exposed by `HTTPServer`:

```python
@server.get("/people")
def list_people():
    return JSONResponse({"people": []})

@server.post("/people/{people_id}/contacts/{contact_id}")
def add_contact(people_id: str, contact_id: str):
    return JSONResponse({"ok": True, "person": people_id, "contact": contact_id})

@server.put("/people/{id}")
def replace_person(id: str):
    return JSONResponse({"replaced": id})
```

**Dynamic params**: Any `{name}` segment is captured and injected as a `str` param.

### 2) Receive the raw headers (optional)

If your handler includes a `headers: Headers` parameter, the framework will inject it:

```python
from src.http.models.headers import Headers

@server.get("/debug")
def debug(headers: Headers):
    return JSONResponse({"headers": str(headers)})
```

### 3) Parse JSON or form bodies into Pydantic models

Declare any parameter **typed as a Pydantic model**. For `POST` and `PUT`, the processor will instantiate the model from the request body automatically.

```python
from pydantic import BaseModel

class Contact(BaseModel):
    name: str
    email: str

@server.post("/people/{people_id}/contacts")
def add_contact(people_id: str, contact: Contact):
    # contact is a Contact instance
    return JSONResponse({"created_for": people_id, "name": contact.name})
```

Supported content types:
- `application/json` — parsed via `json.loads`
- `application/x-www-form-urlencoded` — parsed via `urllib.parse.parse_qs`

> The parser **validates** `Content-Length` and rejects mismatches.

### 4) Return a response

Handlers must return `JSONResponse`. You can attach additional headers if you want:

```python
from src.http.models.response import JSONResponse

@server.get("/with-headers")
def with_headers():
    return JSONResponse(
        content={"ok": True},
        custom_headers={"X-Trace-Id": "abc123"}
    )
```

The server calls `add_required_headers(...)` for you. By default, it sets:

- `Content-Type` → taken from the **request**’s `Content-Type` (see note below)
- `Content-Length` → computed from the JSON body

---

## End-to-end example (server and raw socket client)

**Server:**

```python
from pydantic import BaseModel
from src.http.models.response import JSONResponse
from src.http.models.headers import Headers
from src.http.http_server import HTTPServer

print("creating server")
http_server = HTTPServer()

@http_server.get("/people")
def custom(id: str):
    return JSONResponse(content={"ji": "k"}, custom_headers={"j": "k", "g": "g"})

class User(BaseModel):
    user: str
    age: int

@http_server.post("/people/{people_id}/contacts/{contact_id}")
def custom(people_id: str, contact_id: str):
    return JSONResponse(content={"ji": "k"}, custom_headers={"j": "k", "g": "g"})

@http_server.post("/people/{people_id}/contacts/{contact_id}")
def custom(people_id: str, contact_id: str, user: User):
    print("user", user)
    print("bye", people_id, contact_id)
    return JSONResponse(content={"ji": "k"}, custom_headers={"j": "k", "g": "g"})

print("server created")
http_server.run()
```

**Client (raw sockets):**

```python
import json
import socket

payload = {"user": "John", "age": 10}
body = json.dumps(payload)
content_length = len(body.encode())

s = socket.socket()
s.connect(("127.0.0.1", 80))
s.sendall(
    f"POST /people/123/contacts/1234 HTTP/1.1\r\n"
    f"Content-Type: application/json\r\n"
    f"Content-Length: {content_length}\r\n"
    f"\r\n"
    f"{body}".encode()
)
data = s.recv(1024)
print(data.decode())
s.close()
```

---

## How it works (internals)

- **`TCPServer`**: Opens a socket (defaults to IPv4, port **80**), `accept()` loop, receives **1024 bytes**, calls `handle_request`, and writes back `bytes(response)`.
- **`HTTPServer`**: Owns the `RouterTrie`, `HTTPParser`, and `HTTPProcessor`. Exposes `get/post/put` decorators and orchestrates parsing → dispatch → response.
- **`HTTPParser`**: Validates the request line, headers (against `SupportedHeaders`), enforces `Content-Length`, and parses body based on `Content-Type`.
- **`RouterTrie`**: Inserts paths by segments; supports `{param}` lookup. Stores `{HTTPMethod → handler}` per terminal node.
- **`HTTPProcessor`**: Converts method string to `HTTPMethod`, resolves the handler, builds arguments:
  - Path params from the trie,
  - Body object if the handler has a Pydantic-typed parameter,
  - `headers: Headers` if the handler declares it.
- **`JSONResponse`**: Holds the content and headers, can render to bytes (`__bytes__`).

---

## Configuration & tips

- **Ports/privileges**: Port **80** typically requires elevated privileges. For dev, switch to `8080` in `TCPServer` (adapt the constructor to accept a port).
- **Receive size**: `recv(1024)` is small if you send larger bodies—consider increasing or looping until you read the full payload (`Content-Length`).
- **Headers policy**: By default the response echoes the request’s `Content-Type`. If you want to always return JSON, you can force `application/json` in `JSONResponse`.

---

## Known limitations

- **No HTTP status line** in responses.
- **No general header support** beyond the current minimal set.
- **Single, blocking accept loop** (no concurrency).

