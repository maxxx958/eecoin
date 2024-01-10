from node import Node
from blockchain import hash
import time
node_max4 = Node("max4", 12348)
node_max4.start()
node_max4.register(12345)
while True:
    print(node_max4.chain.blocks[-1][-5:], len(node_max4.chain.blocks))
    time.sleep(5)