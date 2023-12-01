import pickle, base64, random, hashlib, time
magic = "$#$#"
difficulty = 6

def hash(string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode())
    return sha256_hash.hexdigest()

class Blockchain:
    def __init__(self, node):
        self.blocks = ["the starting blockkkkkk"]
        self.node = node
        random.seed(self.node.name)
    
    def mine(self):
        while True:
            self.try_to_add_block()

    def valid(self, block):
        if hash(block)[:difficulty] == "0"*difficulty:
            return True
        return False

    def try_to_add_block(self):
        times = 0
        while True:
            proof_of_work = str(random.randrange(2**64))
            new_block = magic.join([hash(self.blocks[-1]) + "one eecoin for me" + proof_of_work])
            times += 1
            if self.valid(new_block):
                self.blocks.append(new_block)
                self.propagate()
                print(f"[{self.node.name}] I just mined a new block ", hash(new_block), times)
                times = 0
                time.sleep(1)

    def propagate(self):
        self.node.broadcast_new_block(self.blocks_to_string())

    def blocks_to_string(self):
        return base64.b64encode(pickle.dumps(self.blocks)).decode()

    def load_blocks_from_string(self, string):
        new_blocks = pickle.loads(base64.b64decode(string))
        if len(new_blocks) == len(self.blocks) + 1 and new_blocks[-2] == self.blocks[-1]:
            self.blocks = new_blocks
            print("I'm accepting the new block as it is building on what I already have")
        else:
            print("This new chain is bullshit")

# b1 = Blockchain()
# b1.blocks = [1, 2, 3]
# b2 = Blockchain()
# b2.blocks = [3, 2, 1]
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
# b2.load_blocks_from_string(b1.blocks_to_string())
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
