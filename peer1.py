import socket
import threading


def handle_peer2_connection(peer2_socket):
    while True:
        data = peer2_socket.recv(1024)
        if not data:
            print("Peer 2 disconnected.")
            peer2_socket.close()
            break
        print(f"Received from Peer 2: {data.decode()}")
        message = input("Enter a message to send to Peer 2: ")
        peer2_socket.send(message.encode())


# Create a socket for Peer 1
peer1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer1.bind(("localhost", 12345))
peer1.listen(1)

print("Peer 1 is listening on port 12345.")

while True:
    peer2_socket, peer2_address = peer1.accept()
    print(f"Peer 2 connected from {peer2_address}")

    # Create a thread to handle the connection to Peer 2
    peer2_handler = threading.Thread(
        target=handle_peer2_connection, args=(peer2_socket,)
    )
    peer2_handler.start()
