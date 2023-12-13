from node import Node
from blockchain import hash
import time
node_max3 = Node("max3", 12347)
node_max3.start()
node_max3.register(12346)
while True:
    print(node_max3.chain.blocks[-1][-5:], len(node_max3.chain.blocks))
    time.sleep(5)