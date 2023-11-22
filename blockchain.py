import pickle, base64, random, time, hashlib

magic = "$#$#"

def hash(string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode())
    return sha256_hash.hexdigest()

class Blockchain:
    def __init__(self):
        self.blocks = []
        random.seed(time.now())

    def valid(self, block):
        if hash(block)[:2] == "00":
            return True
        return False

    def try_to_add_block(self):
        while True:
            proof_of_work = random.randrange(2**64)
            new_block = magic.join([hash(self.blocks[-1]) + "one eecoin for me" + proof_of_work])
            if self.valid(new_block):
                self.blocks.append(new_block)
                self.propagate()
                print("I just mined a block, taking a break")
                time.sleep(10)

    def propagate(self):
        pass

    def blocks_to_string(self):
        return base64.b64encode(pickle.dumps(self.blocks)).decode()

    def load_blocks_from_string(self, string):
        self.blocks = pickle.loads(base64.b64decode(string))

# b1 = Blockchain()
# b1.blocks = [1, 2, 3]
# b2 = Blockchain()
# b2.blocks = [3, 2, 1]
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
# b2.load_blocks_from_string(b1.blocks_to_string())
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
