import socket
import ssl

class web_info:
    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port

    def verify_ssl(self) -> int:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_default_certs()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                ssl_sock = context.wrap_socket(sock, server_hostname=self.hostname)
                ssl_sock.connect((self.hostname, self.port))
                ssl_sock.close()
        except Exception as e:
            return 0
        return 1