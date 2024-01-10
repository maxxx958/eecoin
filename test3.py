from node import Node
import time
node_max3 = Node("max3", 12347)
node_max3.start()
node_max3.register(12346)
while True:
    longest_idx = 0
    for i in range(len(node_max3.chain.chains)):
        if len(node_max3.chain.chains[i]) > len(node_max3.chain.chains[longest_idx]):
            longest_idx = i
    print("[max3]\t", node_max3.chain.chains[longest_idx][-1][-5:], len(node_max3.chain.chains[longest_idx]), len(node_max3.chain.chains))
    time.sleep(5)