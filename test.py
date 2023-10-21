from node import Node

node_max = Node("max", 12345)
node_max.start()
node_kacper = Node("kacper", 54321)
node_kacper.start()
node_kacper.register(12345)
