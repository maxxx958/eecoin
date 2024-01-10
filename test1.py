from node import Node
import time
node_max = Node("max", 12345)
node_max.start()
while True:
    longest_idx = 0
    for i in range(len(node_max.chain.chains)):
        if len(node_max.chain.chains[i]) > len(node_max.chain.chains[longest_idx]):
            longest_idx = i
    print("[max]\t", node_max.chain.chains[longest_idx][-1][-5:], len(node_max.chain.chains[longest_idx]), len(node_max.chain.chains))
    time.sleep(5)
