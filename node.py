import socket, threading, crypto, json, base64

magic = "$#$#"

class Node:
    def __init__(self, name, port, password=None):
        self.port = port
        self.name = name
        self.peers = []
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.privkey, self.pubkey = crypto.generate_key_pair()
    

    def start(self):
        self.listen_socket.bind(("localhost", self.port))
        self.listen_socket.listen(10)
        print(f"Node {self.name} is listening on port {self.port}.")
        threading.Thread(target=self.accept_connections).start()


    def accept_connections(self):
        while True:
            peer_socket, peer_address = self.listen_socket.accept()
            print(f"{self.name}: Peer connected to me from {peer_address}")
            self.peers.append(peer_socket)
            threading.Thread(target=self.handle_request, args=(peer_socket,)).start()


    def handle_request(self, peer_socket):
        packet = peer_socket.recv(4096).decode().split(magic)
        if not packet:
            return
        # for key, value in packet.items():
        #     if key in ["pubkey", "signature"]:
        #         packet[key] = base64.b64decode(value.encode())
        if packet[0] == "send":
            self.handle_send(packet, peer_socket)
        elif packet[0] == "register":
            self.handle_register(packet[1:], peer_socket)
        else:
            peer_socket.send(magic.join(["response", "Error: unknown header"]).encode())
            peer_socket.close()


    def handle_register(self, packet, peer_socket):
        name, pubkey, port, signature = packet
        port = int(port)
        if crypto.verify_signature_with_public_key(pubkey, name, signature):
            self.peers.append({"name": name, "pubkey": pubkey, "port": port})
            print(f"{self.name}: I just registered a new guy:\n{self.peers[-1]}.\n")
            peer_socket.send(magic.join(["response", "Success: you got registered bro, happy minin'!"]).encode())
            # and now let everyone know about the new guy
        else:
            peer_socket.send(magic.join(["response", "Error: keys don't match, get lost hacker!"]).encode())
        peer_socket.close()


    def handle_send(self, packet, peer_socket):
        name, data = packet
        print(f"{self.name}: Received data from {name}\n{data}\n")
        peer_socket.close()


    def send(self, data, port):
        connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        packet = {
            "header": "send",
            "name": self.name,
            "data": data,
            "signature": crypto.sign_with_private_key(data, self.privkey)
        }
        try:
            connecting_socket.connect(("localhost", port))
            connecting_socket.send(json.dumps(packet))
        except:
            print("Lost connection to peer when sending data.")
        connecting_socket.close()


    def register(self, port):
        # send a packet with your name, public_key and your name signed with your private_key
        registering_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        packet = [
            "register",
            self.name,
            self.pubkey.decode(),
            str(self.port),
            base64.b64encode(crypto.sign_with_private_key(self.privkey, self.name)).decode()
        ]
        try:
            registering_socket.connect(("localhost", port))
            registering_socket.send(magic.join(packet).encode())
            response = registering_socket.recv(4096).decode().split(magic)
            print(f"{self.name}: I got this response after registering:\n{response}\n")
        except Exception as e:
            print(f"Lost connection to peer when registering. {e}")
        registering_socket.close()