import socket, threading, crypto, json, base64

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
        packet = json.loads(peer_socket.recv(4096).decode("utf-8"))
        if not packet:
            return
        for key, value in packet.items():
            if key in ["pubkey", "signature"]:
                packet[key] = base64.b64decode(value.encode("utf-8"))
        if packet["header"] == "send":
            self.handle_send(packet, peer_socket)
        elif packet["header"] == "register":
            self.handle_register(packet, peer_socket)
        else:
            peer_socket.send(json.dumps({"header": "response", "message": "Error: unknown header"}))
            peer_socket.close()


    def handle_register(self, packet, peer_socket):
        if crypto.verify_signature_with_public_key(packet["pubkey"], packet["name"], packet["signature"]):
            self.peers.append({"name": packet["name"], "pubkey": packet["pubkey"], "port": packet["port"]})
            print(f"{self.name}: I just registered a new guy:\n{self.peers[-1]}.\n")
            peer_socket.send(json.dumps({"header": "response", "message": "Success: you got registered bro, happy minin'!"}).encode("utf-8"))
            # and now let everyone know about the new guy
        else:
            peer_socket.send(json.dumps({"header": "response", "message": "Error: keys don't match, get lost hacker!"}).encode("utf-8"))
        peer_socket.close()
    

    def handle_send(self, packet, peer_socket):
        print(f"{self.name}: Received data from {packet['name']}\n{packet['data']}\n")
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
        packet = {
            "header": "register",
            "name": self.name,
            "pubkey": base64.b64encode(self.pubkey).decode("utf-8"),
            "port": self.port,
            "signature": base64.b64encode(crypto.sign_with_private_key(self.privkey, self.name)).decode("utf-8")
        }
        try:
            registering_socket.connect(("localhost", port))
            registering_socket.send(json.dumps(packet).encode("utf-8"))
            response = json.loads(registering_socket.recv(4096))
            print(f"{self.name}: I got this response after registering:\n{response}\n")
        except Exception as e:
            print(f"Lost connection to peer when registering. {e}")
        registering_socket.close()