from node import Node
import time
node_max5 = Node("max5", 12349)
node_max5.start()
node_max5.register(12348)
while True:
    longest_idx = 0
    for i in range(len(node_max5.chain.chains)):
        if len(node_max5.chain.chains[i]) > len(node_max5.chain.chains[longest_idx]):
            longest_idx = i
    print("[max5]\t", node_max5.chain.chains[longest_idx][-1][-5:], len(node_max5.chain.chains[longest_idx]), len(node_max5.chain.chains))
    time.sleep(5)