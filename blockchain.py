import pickle, base64, random, hashlib, time, threading, binascii
magic = "$#$#"
difficulty = 20
block_size = 5

def hash(string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode())
    return sha256_hash.hexdigest()

class Blockchain:
    def __init__(self, node):
        self.blocks = [magic.join(["0", "system system 0.0", "0"])]
        self.transactions = []
        self.node = node
        self.lock = node.lock
        random.seed(self.node.name)
        self.wallets = {"system": 0.0}
    
    def mine(self):
        while True:
            self.try_to_add_block()

    def valid(self, block):
        hash_bytes = binascii.unhexlify(hash(block))
        binary_string = ''.join(format(byte, '08b') for byte in hash_bytes)
        if binary_string[:difficulty] == "0"*difficulty:
            return True
        return False

    def receive_transaction(self, transaction):
        # print(f"[{self.node.name}] Got it!")
        self.transactions.append(transaction)

    def pick_transactions(self):
        new_wallets = dict(self.wallets)
        possible_transactions = []
        with self.lock:
            for transaction in self.transactions:
                sender, receiver, amount = transaction.split()
                amount = float(amount)
                if new_wallets.get(sender, 0) >= amount:
                    new_wallets[receiver] = new_wallets.get(receiver, 0) + amount
                    new_wallets[sender] -= amount
                    possible_transactions.append(transaction)
                    if len(possible_transactions) == block_size:
                        return possible_transactions
        return possible_transactions


    def try_to_add_block(self):
        times = 0
        while True:
            proof_of_work = str(random.randrange(2**64))
            new_block = magic.join([hash(self.blocks[-1]), magic.join(self.pick_transactions()), f"system {hash(self.node.pubkey)} 10.0", proof_of_work])
            times += 1
            if self.valid(new_block):
                self.blocks.append(new_block)
                self.node.broadcast_new_block(self.block_to_string(new_block))
                print(f"[{self.node.name}]\tI just mined a new block ", new_block, times)
                self.update_wallets(new_block)
                # print("wallets:", self.wallets)
                times = 0
                self.transactions = self.transactions[block_size:]
                # time.sleep(1)

    def blocks_to_string(self):
        return base64.b64encode(pickle.dumps(self.blocks)).decode()

    def block_to_string(self, block):
        return base64.b64encode(pickle.dumps(block)).decode()

    def update_wallets(self, block):
        for transaction in block.split(magic)[1:-1]:
            if len(transaction) == 0:
                continue
            sender, recipient, amount = transaction.split()
            amount = float(amount)
            if sender == "system" or self.wallets.get(sender, 0) >= amount:
                self.wallets[recipient] = self.wallets.get(recipient, 0) + amount
                self.wallets[sender] -= amount
            else:
                raise Exception(f"Sender ({sender}) has insufficient funds for this transaction.")

    def load_blocks_from_string(self, string):
        new_blocks = pickle.loads(base64.b64decode(string))
        if len(new_blocks) > len(self.blocks):
            self.blocks = new_blocks
            for block in self.blocks:
                self.update_wallets(block)
            print(f"[{self.node.name}]\tACCEPT, I'm accepting the new chain as it's longer than mine :P.")
            # print("wallets:", self.wallets)
        else:
            print(f"[{self.node.name}]\tREJECT, It's not longer, I'm keeping mine.", len(new_blocks), len(self.blocks))
            if new_blocks != self.block_to_string:
                print(f"[{self.node.name}]\tThey are even different.")
        return
        if len(new_blocks) >= len(self.blocks) and new_blocks[:len(self.blocks)] == self.blocks:
            self.blocks = new_blocks
            print(f"[{self.node.name}]\tI'm accepting the new chain as it is longer version of what I already have.")
        else:
            print(f"[{self.node.name}]\tThis new chain is bullshit.")
    
    def load_block_from_string(self, string):
        new_block = pickle.loads(base64.b64decode(string))
        prev_hash = new_block.split(magic)[0]
        if prev_hash == hash(self.blocks[-1]):
            for transaction in new_block.split(magic)[1:-2]:
                if transaction in self.transactions:
                    self.transactions.remove(transaction)
            self.blocks.append(new_block)
            self.update_wallets(new_block)
            self.node.broadcast_new_block(self.block_to_string(new_block))
            print(f"[{self.node.name}]\tACCEPT, I'm accepting the new block as it is building on what I already have.")
            # print("wallets:", self.wallets)
            return True
        elif new_block == self.blocks[-1]:
            print(f"[{self.node.name}]\tIDC, I already have this block.")
            return True
        else:
            print(f"[{self.node.name}]\tASKING, I'm asking for more blocks.")
        return False
        #print(f"[{self.node.name}]\tERROR: This new block is bullshit, ignoring.")

# b1 = Blockchain()
# b1.blocks = [1, 2, 3]
# b2 = Blockchain()
# b2.blocks = [3, 2, 1]
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
# b2.load_blocks_from_string(b1.blocks_to_string())
# print(b1.blocks_to_string())
# print(b2.blocks_to_string())
