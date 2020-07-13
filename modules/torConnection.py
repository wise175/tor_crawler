from stem import Signal
from stem.control import Controller
import socks, socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9050


class TorConnection:

    @staticmethod
    def tor_connect(host, port):
        if not host:
            host = DEFAULT_HOST
        if not port:
            port = DEFAULT_PORT

        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="tor_crawler")
            controller.signal(Signal.NEWNYM)

        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, host, port)
        socket.socket = socks.socksocket

        def getaddrinfo(*args):
            return [
                (socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

        socket.getaddrinfo = getaddrinfo

