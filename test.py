from node import Node
import time

# node_max = Node("max", 12345)
# node_max.start()
# node_kacper = Node("kacper", 54321)
# node_kacper.start()
# node_kacper.register(12345)

# node_max.send("elo elo", 54321)

# node_bartek = Node("bartek", 33333)
# node_bartek.start()
# node_bartek.register(54321)

# node_patryk = Node("patryk", 33331)
# node_patryk.start()
# node_patryk.register(33333)

# if not (node_max.peers == node_kacper.peers == node_bartek.peers == node_patryk.peers):
#     print("Jeszcze nie działa")

# time.sleep(1)

# if node_max.peers == node_kacper.peers == node_bartek.peers == node_patryk.peers:
#     print("Działa, wszyscy mają takich samych peerów")

node_max = Node("max", 12345)
node_max.start()
time.sleep(5)
node_max2 = Node("max2", 12346)
node_max2.start()
node_max2.register(12345)
time.sleep(1)
node_max.broadcast_transaction("max max2 1.0")
node_max2.broadcast_transaction("max max2 2.0")
node_max.broadcast_transaction("max max2 3.0")
node_max2.broadcast_transaction("max max2 4.0")
node_max.broadcast_transaction("max max2 5.0")
node_max2.broadcast_transaction("max max2 6.0")
node_max.broadcast_transaction("max max2 7.0")
node_max2.broadcast_transaction("max max2 8.0")
node_max.broadcast_transaction("max max2 9.0")
node_max2.broadcast_transaction("max max2 10.0")
node_max2.broadcast_transaction("max max2 11.0")
time.sleep(10)
print(node_max2.chain.transactions)
print(node_max.chain.transactions)
print(node_max.chain.blocks)

