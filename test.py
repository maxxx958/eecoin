from node import Node
import time

node_max = Node("max", 12345)
node_max.start()
node_kacper = Node("kacper", 54321)
node_kacper.start()
node_kacper.register(12345)

node_max.send("elo elo", 54321)

node_bartek = Node("bartek", 33333)
node_bartek.start()
node_bartek.register(54321)

node_patryk = Node("patryk", 33331)
node_patryk.start()
node_patryk.register(33333)

if not (node_max.peers == node_kacper.peers == node_bartek.peers == node_patryk.peers):
    print("Jeszcze nie działa")

time.sleep(1)

if node_max.peers == node_kacper.peers == node_bartek.peers == node_patryk.peers:
    print("Działa, wszyscy mają takich samych peerów")