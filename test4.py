from node import Node
import time
node_max4 = Node("max4", 12348)
node_max4.start()
node_max4.register(12345)
while True:
    longest_idx = 0
    for i in range(len(node_max4.chain.chains)):
        if len(node_max4.chain.chains[i]) > len(node_max4.chain.chains[longest_idx]):
            longest_idx = i
    print("[max4]\t", node_max4.chain.chains[longest_idx][-1][-5:], len(node_max4.chain.chains[longest_idx]), len(node_max4.chain.chains))
    time.sleep(5)