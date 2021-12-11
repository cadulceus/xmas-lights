import socket
from pickle import dumps

class tree:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

    def write_pixels(self, pixels):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.send(dumps(pixels))
            s.close()