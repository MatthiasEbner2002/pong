import socket
import pickle

class Network:
    def __init__(self, is_server=False, server_ip=None, start_now=True):
        self.is_server = is_server
        self.server_ip = server_ip
        self.host = None
        self.server_socket = None
        self.client_socket = None
        self.port = 5555

        if start_now:
            if self.is_server:
                self.start_server()
            else:
                self.connect_to_server()

    def start_server(self):
        self.start_socket()
        self.accept_connection()

    def connect_to_server(self):
        self.host = self.server_ip
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host,  self.port))
        print("Connected to", self.host)

    def send_data(self, data):
        data_bytes = pickle.dumps(data)
        self.client_socket.send(data_bytes)

    def receive_data(self):
        data_bytes = self.client_socket.recv(4096)
        data = pickle.loads(data_bytes)
        return data

    def close_connection(self):
        self.client_socket.close()
        if self.is_server:
            self.server_socket.close()
            
    def start_socket(self):
        self.host = socket.gethostbyname(self.get_ip_address())
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host,  self.port))
        self.server_socket.listen(1)    # 1 is the maximum number of connections
        print(f"Waiting for a connection...{self.host}")
        return self.host
        
        
    def accept_connection(self):
        self.client_socket, addr = self.server_socket.accept()
        print("Connected to", addr)

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        address = s.getsockname()[0]
        s.close()
        return address
    
    def __str__(self):
        return f"Network(is_server={self.is_server}, server_ip={self.server_ip}, host={self.host}, port={self.port}, server_socket={self.server_socket}, client_socket={self.client_socket})"
        