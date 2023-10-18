import socket

# Create a socket for Peer 2
peer2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer2.connect(("localhost", 12345))

while True:
    message = input("Enter a message to send to Peer 1: ")
    peer2.send(message.encode())
    data = peer2.recv(1024)
    print(f"Received from Peer 1: {data.decode()}")
