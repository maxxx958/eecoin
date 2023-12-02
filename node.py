import socket, threading, crypto, base64, blockchain

magic = "$#$#"
verbose = False

class Node:
    def __init__(self, name, port, password=None, miner=True):
        self.port = port
        self.name = name
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.privkey, self.pubkey = crypto.generate_key_pair()
        self.pubkey = self.pubkey.decode()
        self.peers = set()
        self.peers.add((self.name, self.pubkey, self.port))
        self.lock = threading.Lock()
        self.chain = blockchain.Blockchain(self)
        self.miner = miner
        
    
    def start(self):
        self.listen_socket.bind(("localhost", self.port))
        self.listen_socket.listen(10)
        if verbose:
            print(f"[{self.name}] I'm listening on port {self.port}.")
        threading.Thread(target=self.accept_connections).start()
        if self.miner:
            threading.Thread(target=self.chain.mine, args=(self.lock,)).start()


    def accept_connections(self):
        while True:
            peer_socket, peer_address = self.listen_socket.accept()
            if verbose:
                print(f"[{self.name}] Peer connected to me from {peer_address}")
            threading.Thread(target=self.handle_request, args=(peer_socket,)).start()


    def handle_request(self, peer_socket):
        packet = peer_socket.recv(16384).decode().split(magic)
        if not packet:
            return
        if packet[0] == "new_block":
            self.handle_send_new_block(packet[1:], peer_socket)
        elif packet[0] == "blocks":
            self.handle_send_blocks(packet[1:], peer_socket)
        elif packet[0] == "transaction":
            self.handle_send_transaction(packet[1:], peer_socket)
        elif packet[0] == "register":
            self.handle_register(packet[1:], peer_socket)
        elif packet[0] == "new_peer":
            self.handle_pass_new_peer(packet[1:])
        else:
            peer_socket.send(magic.join(["response", "Error: unknown header"]).encode())
            peer_socket.close()


    def handle_register(self, packet, peer_socket):
        name, pubkey, port, signature = packet
        port = int(port)
        if crypto.verify_signature_with_public_key(pubkey, name, signature):
            peers_pack = ["Success"]
            self.lock.acquire()
            for peer in self.peers:
                peers_pack += list(peer)
                peers_pack[-1] = str(peers_pack[-1])
            self.lock.release()
            peer_socket.send(magic.join(peers_pack).encode())
            self.pass_new_peer(name, pubkey, port)
            self.send_blocks(port)
        else:
            peer_socket.send("Error: keys don't match, get lost hacker!".encode())
        peer_socket.close()

    def handle_pass_new_peer(self, packet):
        name, pubkey, port = packet
        self.lock.acquire()
        self.peers.add((name, pubkey, int(port)))
        self.lock.release()

    def handle_send_new_block(self, packet, peer_socket):
        try:
            name, data, signature = packet
        except:
            print(f"[{self.name}] Incorrect packet format.")
        pubkey = None
        self.lock.acquire()
        for peer in self.peers:
            p_name, p_pubkey, _ = peer
            if p_name == name:
                pubkey = p_pubkey
                break
        self.lock.release()
        if crypto.verify_signature_with_public_key(pubkey, data, signature):
            if verbose:
                print(f"[{self.name}] Received data from {name}\n{data}")
            self.chain.load_block_from_string(data)
        else:
            print(f"[{self.name}] Incorrect signature, can't verify the message from {name}.")
        peer_socket.close()
    
    def handle_send_transaction(self, packet, peer_socket):
        try:
            name, data, signature = packet
        except:
            print(f"[{self.name}] Incorrect packet format.")
        pubkey = None
        self.lock.acquire()
        for peer in self.peers:
            p_name, p_pubkey, _ = peer
            if p_name == name:
                pubkey = p_pubkey
                break
        self.lock.release()
        if crypto.verify_signature_with_public_key(pubkey, data, signature):
            if verbose:
                print(f"[{self.name}] Received data from {name}\n{data}")
            self.chain.receive_transaction(data)
        else:
            print(f"[{self.name}] Incorrect signature, can't verify the message from {name}.")
        peer_socket.close()
    
    def handle_send_blocks(self, packet, peer_socket):
        try:
            name, data, signature = packet
        except:
            print(f"[{self.name}] Incorrect packet format.")
        pubkey = None
        self.lock.acquire()
        for peer in self.peers:
            p_name, p_pubkey, _ = peer
            if p_name == name:
                pubkey = p_pubkey
                break
        self.lock.release()
        if crypto.verify_signature_with_public_key(pubkey, data, signature):
            if verbose:
                print(f"[{self.name}] Received data from {name}\n{data}")
            self.chain.load_blocks_from_string(data)
        else:
            print(f"[{self.name}] Incorrect signature, can't verify the message from {name}.")
        peer_socket.close()

    def send_new_block(self, data, port):
        connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        packet = [
            "new_block",
            self.name,
            data,
            base64.b64encode(crypto.sign_with_private_key(self.privkey, data)).decode()
        ]
        try:
            connecting_socket.connect(("localhost", port))
            connecting_socket.send(magic.join(packet).encode())
        except Exception as e:
            print(f"[{self.name}] Lost connection to peer when sending data {e}.")
        connecting_socket.close()
    
    def broadcast_new_block(self, data):
        self.lock.acquire()
        for name, _, port in self.peers:
            if name != self.name:
                self.send_new_block(data, port)
        self.lock.release()
    
    def send_blocks(self, port):
        connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = self.chain.blocks_to_string()
        packet = [
            "blocks",
            self.name,
            data,
            base64.b64encode(crypto.sign_with_private_key(self.privkey, data)).decode()
        ]
        try:
            connecting_socket.connect(("localhost", port))
            connecting_socket.send(magic.join(packet).encode())
        except Exception as e:
            print(f"[{self.name}] Lost connection to peer when sending data {e}.")
        connecting_socket.close()

    def pass_new_peer(self, name, pubkey, port):
        self.lock.acquire()
        for peer in self.peers:
            _, _, p_port = peer
            connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            packet = [
                "new_peer",
                name,
                pubkey,
                str(port)
            ]
            try:
                connecting_socket.connect(("localhost", p_port))
                connecting_socket.send(magic.join(packet).encode())
            except Exception as e:
                print(f"[{self.name}] Couldn't pass new peer {e}.")
            connecting_socket.close()
        self.lock.release()


    def register(self, port):
        registering_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        packet = [
            "register",
            self.name,
            self.pubkey,
            str(self.port),
            base64.b64encode(crypto.sign_with_private_key(self.privkey, self.name)).decode()
        ]
        try:
            registering_socket.connect(("localhost", port))
            registering_socket.send(magic.join(packet).encode())
            response = registering_socket.recv(16384).decode().split(magic)
            if response[0] == "Success":
                response = response[1:]
                for i in range(0, len(response), 3):
                    peer = response[i : i + 3]
                    peer[2] = int(peer[2])
                    self.lock.acquire()
                    self.peers.add(tuple(peer))
                    self.lock.release()
                    if verbose:
                        print(f"[{self.name}] I'm adding {peer[0]} to my peers.")
            else:
                print(f"[{self.name}] {response[0]}")
        except Exception as e:
            print(f"[{self.name}] Lost connection to peer when registering {e}.")
        registering_socket.close()
    
    def send_transaction(self, content, port):
        connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        packet = [
            "transaction",
            self.name,
            content,
            base64.b64encode(crypto.sign_with_private_key(self.privkey, content)).decode()
        ]
        try:
            connecting_socket.connect(("localhost", port))
            connecting_socket.send(magic.join(packet).encode())
        except Exception as e:
            print(f"[{self.name}] Lost connection to peer when sending transaction {e}.")
        connecting_socket.close()

    def broadcast_transaction(self, content):
        self.lock.acquire()
        for _, _, port in self.peers:
            self.send_transaction(content, port)
        self.lock.release()