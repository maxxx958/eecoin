from node import Node
from blockchain import hash
import time
node_max2 = Node("max2", 12346)
node_max2.start()
node_max2.register(12345)
while True:
    print(node_max2.chain.blocks[-1][-5:], len(node_max2.chain.blocks))
    time.sleep(5)
