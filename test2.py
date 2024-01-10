from node import Node
import time
node_max2 = Node("max2", 12346)
node_max2.start()
node_max2.register(12345)
while True:
    longest_idx = 0
    for i in range(len(node_max2.chain.chains)):
        if len(node_max2.chain.chains[i]) > len(node_max2.chain.chains[longest_idx]):
            longest_idx = i
    print("[max2]\t", node_max2.chain.chains[longest_idx][-1][-5:], len(node_max2.chain.chains[longest_idx]), len(node_max2.chain.chains))
    time.sleep(5)
