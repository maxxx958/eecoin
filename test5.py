from node import Node
from blockchain import hash
import time
node_max5 = Node("max5", 12349)
node_max5.start()
node_max5.register(12348)
while True:
    print(node_max5.chain.blocks[-1][-5:], len(node_max5.chain.blocks))
    time.sleep(5)