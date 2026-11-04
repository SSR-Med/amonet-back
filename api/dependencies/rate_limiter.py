from slowapi import Limiter
from slowapi.util import get_remote_address


def client_ip(request) -> str:
    return request.headers.get("cf-connecting-ip") or get_remote_address(request)


limiter = Limiter(key_func=client_ip)
