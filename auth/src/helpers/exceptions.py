class AuthException(Exception):
    def __init__(self, message: str = None, status_code: int = None):
        self.message = message
        self.status_code = status_code
