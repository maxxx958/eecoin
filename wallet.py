import socket, threading


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.start()

    def connect(self, host, port):
        try:
            connection = self.socket.connect((host, port))
            self.connections.append(connection)
            print(f"Successfully connected to {host}:{port}.")
        except socket.error as err:
            print(f"Failed to connect to {host}:{port}. Error: {err}.")

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}.")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}.")

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as err:
                print(f"Failed to send data. Error: {err}.")
        print(f"Finished sending the data to {len(self.connections)} users.")

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


peer1 = Peer("localhost", 12345)
peer2 = Peer("localhost", 54321)

from time import sleep

sleep(1)
peer2.connect("localhost", 12345)
peer1.connect("localhost", 54321)
sleep(1)
peer2.send_data("hello world")
