import pickle, base64, random, hashlib, time
magic = "$#$#"
difficulty = 5
block_size = 5

def hash(string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode())
    return sha256_hash.hexdigest()

class Blockchain:
    def __init__(self, node):
        self.blocks = ["the starting block"]
        self.transactions = []
        self.node = node
        random.seed(self.node.name)
    
    def mine(self, lock):
        while True:
            self.try_to_add_block()

    def valid(self, block):
        if hash(block)[:difficulty] == "0"*difficulty:
            return True
        return False

    def receive_transaction(self, transaction):
        print(f"[{self.node.name}] Got it!")
        self.transactions.append(transaction)

    def try_to_add_block(self):
        times = 0
        while len(self.transactions) >= block_size:
            proof_of_work = str(random.randrange(2**64))
            new_block = magic.join([hash(self.blocks[-1]), magic.join(self.transactions[:block_size]), f"system {self.node.name} 1.0", proof_of_work])
            times += 1
            if self.valid(new_block):
                self.blocks.append(new_block)
                self.node.broadcast_new_block(self.block_to_string())
                print(f"[{self.node.name}]\tI just mined a new block ", hash(new_block), times)
                times = 0
                self.transactions = self.transactions[block_size:]
                time.sleep(1)

    def blocks_to_string(self):
        return base64.b64encode(pickle.dumps(self.blocks)).decode()

    def block_to_string(self):
        return base64.b64encode(pickle.dumps(self.blocks[-1])).decode()

    def load_blocks_from_string(self, string):
        new_blocks = pickle.loads(base64.b64decode(string))
        self.blocks = new_blocks
        print(f"[{self.node.name}]\tI'm accepting the new chain as I'm new here and I know nothing :P.")
        return
        if len(new_blocks) >= len(self.blocks) and new_blocks[:len(self.blocks)] == self.blocks:
            self.blocks = new_blocks
            print(f"[{self.node.name}]\tI'm accepting the new chain as it is longer version of what I already have.")
        else:
            print(f"[{self.node.name}]\tThis new chain is bullshit.")
    
    def load_block_from_string(self, string):
        new_block = pickle.loads(base64.b64decode(string))
        for transaction in new_block.split(magic)[1:-2]:
            self.transactions.remove(transaction)
        prev_hash = new_block.split(magic)[0]
        if prev_hash == hash(self.blocks[-1]):
            self.blocks.append(new_block)
            print(f"[{self.node.name}]\tI'm accepting the new block as it is building on what I already have.")
        else:
            print(f"[{self.node.name}]\tERROR: This new block is bullshit.")

# b1 = Blockchain()
# b1.blocks = [1, 2, 3]
# b2 = Blockchain()
# b2.blocks = [3, 2, 1]
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
# b2.load_blocks_from_string(b1.blocks_to_string())
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
