from node import Node
from blockchain import hash
import time
node_max = Node("max", 12345)
node_max.start()
while True:
    print(node_max.chain.blocks[-1][-5:], len(node_max.chain.blocks))
    time.sleep(5)
