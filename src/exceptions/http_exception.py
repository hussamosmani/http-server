class HTTPMethodException(Exception):
    def __init__(self, method):
        super().__init__(f"Invalid method: {method}")
