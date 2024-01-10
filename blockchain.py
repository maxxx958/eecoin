import pickle, base64, random, hashlib, time, threading, binascii
magic = "$#$#"
difficulty = 20
block_size = 5
max_len_diff = 5

def hash(string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode())
    return sha256_hash.hexdigest()

class Blockchain:
    def __init__(self, node):
        self.chains = [[magic.join(["0", "system system 0.0", "0"])]]
        self.transactions = set()
        self.node = node
        self.lock = node.lock
        random.seed(self.node.name)
    
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
        if transaction not in self.transactions:
            self.transactions.add(transaction)

    def pick_transactions(self, chain):
        wallets = {"system": 0.0}
        processed_transactions = set()
        for block in chain:
            for transaction in block.split(magic)[1:-1]:
                if len(transaction) == 0:
                    continue
                processed_transactions.add(transaction)
                sender, recipient, amount = transaction.split()
                amount = float(amount)
                if sender == "system" or wallets.get(sender, 0) >= amount:
                    wallets[recipient] = wallets.get(recipient, 0) + amount
                    wallets[sender] -= amount
                else:
                    raise Exception(f"Sender ({sender}) has insufficient funds for this transaction.")
        possible_transactions = set()
        with self.lock:
            for transaction in self.transactions:
                if transaction in processed_transactions:
                    continue
                sender, receiver, amount = transaction.split()
                amount = float(amount)
                if wallets.get(sender, 0) >= amount:
                    wallets[receiver] = wallets.get(receiver, 0) + amount
                    wallets[sender] -= amount
                    possible_transactions.add(transaction)
                    if len(possible_transactions) == block_size:
                        return possible_transactions
        return list(possible_transactions)

    def try_to_add_block(self):
        times = 0
        while True:
            longest_idx = 0
            for i in range(len(self.chains)):
                if len(self.chains[i]) > len(self.chains[longest_idx]):
                    longest_idx = i
            proof_of_work = str(random.randrange(2**64))
            new_block = magic.join([hash(self.chains[longest_idx][-1]), magic.join(self.pick_transactions(self.chains[longest_idx])), f"system {hash(self.node.pubkey)} 10.0", proof_of_work])
            times += 1
            if self.valid(new_block):
                print(f"[{self.node.name}]\tmined one lol")
                self.chains[longest_idx].append(new_block)
                self.node.broadcast_new_block(self.block_to_string(new_block))
                times = 0

    def chain_to_string(self):
        longest_idx = 0
        for i in range(len(self.chains)):
            if len(self.chains[i]) > len(self.chains[longest_idx]):
                longest_idx = i
        return base64.b64encode(pickle.dumps(self.chains[longest_idx])).decode()

    def block_to_string(self, block):
        return base64.b64encode(pickle.dumps(block)).decode()

    def valid_chain(self, chain):
        wallets = {"system": 0.0}
        for block in chain:
            for transaction in block.split(magic)[1:-1]:
                if len(transaction) == 0:
                    continue
                sender, recipient, amount = transaction.split()
                amount = float(amount)
                if sender == "system" or wallets.get(sender, 0) >= amount:
                    wallets[recipient] = wallets.get(recipient, 0) + amount
                    wallets[sender] -= amount
                else:
                    raise Exception(f"Sender ({sender}) has insufficient funds for this transaction.")
        return True

    def load_blocks_from_string(self, string):
        new_blocks = pickle.loads(base64.b64decode(string))
        print(f"[{self.node.name}]\treceived {len(new_blocks)}")
        longest_length = max(len(chain) for chain in self.chains)
        if len(new_blocks) >= longest_length - max_len_diff and new_blocks not in self.chains:
            self.chains.append(new_blocks)
            print(f"[{self.node.name}]\tACCEPT, I'm accepting the new chain as it's longer than mine :P.")
            return
        if new_blocks not in self.chains:
            print(f"[{self.node.name}]\tToo short")
        elif len(new_blocks) >= longest_length - max_len_diff:
            print(f"[{self.node.name}]\talready have it, why was the block sent")
        return
    
    def load_block_from_string(self, string):
        new_block = pickle.loads(base64.b64decode(string))
        prev_hash = new_block.split(magic)[0]
        self.delete_too_short()
        for chain in self.chains:
            if prev_hash == hash(chain[-1]):
                if self.valid_chain(chain + [new_block]):
                    chain.append(new_block)
                self.node.broadcast_new_block(self.block_to_string(new_block))
                # print(f"[{self.node.name}]\tfits", len(chain))
                return True
            elif new_block == chain[-1]:
                return True
        return False
    
    def delete_too_short(self):
        longest_length = max(len(chain) for chain in self.chains)
        new_chains = list()
        for chain in self.chains:
            if len(chain) >= longest_length - max_len_diff:
                new_chains.append(chain)
        self.chains = new_chains
