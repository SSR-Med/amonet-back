class DomainException(Exception):
    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        self.code = code
        self.message = message
        super().__init__(self.message)
