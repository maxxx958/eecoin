from node import Node
from blockchain import hash
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
#time.sleep(5)
node_max2 = Node("max2", 12346)
node_max2.start()
node_max2.register(12345)
time.sleep(1)
node_max3 = Node("max3", 12347)
node_max3.start()
node_max3.register(12346)

node_max4 = Node("max4", 12348)
node_max4.start()
node_max4.register(12346)

node_max5 = Node("max5", 12349)
node_max5.start()
node_max5.register(12346)
node_max.broadcast_transaction("max2", 1.0)
node_max2.broadcast_transaction("max", 2.0)
node_max.broadcast_transaction("max2", 3.0)
node_max2.broadcast_transaction("max", 4.0)
node_max.broadcast_transaction("max2", 5.0)
node_max2.broadcast_transaction("max", 6.0)
node_max.broadcast_transaction("max2", 7.0)
node_max2.broadcast_transaction("max", 8.0)
node_max.broadcast_transaction("max2", 9.0)
node_max2.broadcast_transaction("max", 10.0)
node_max2.broadcast_transaction("max", 11.0)
while True:
    print(node_max.chain.blocks[-1][-5:], len(node_max.chain.blocks))
    print(node_max2.chain.blocks[-1][-5:], len(node_max2.chain.blocks))
    print(node_max3.chain.blocks[-1][-5:], len(node_max3.chain.blocks))
    print(node_max4.chain.blocks[-1][-5:], len(node_max4.chain.blocks))
    print(node_max5.chain.blocks[-1][-5:], len(node_max5.chain.blocks))
    print(node_max.chain.wallets)
    time.sleep(5)
# time.sleep(10)
# print("transactions in max:\t\t", node_max.chain.transactions)
# print("transactions in max2:\t\t", node_max2.chain.transactions)
# print("current blockchain:\t\t", node_max.chain.blocks)
# print()
# time.sleep(25)
# print("transactions in max:\t\t", node_max.chain.transactions)
# print("transactions in max2:\t\t", node_max2.chain.transactions)
# print("current blockchain:\t\t", node_max.chain.blocks)


'''
OUTPUT:

$ python test.py
[max2]  I'm accepting the new chain as I'm new here and I know nothing :P.
[max2]  I just mined a new block  0000001d970e440955f0a91b64b3e771663decc68e98acba4e9644874c491c80 3138313
wallets: {'system': -1.0, 'max': 997.0, 'max2': 1004.0}
[max]   I'm accepting the new block as it is building on what I already have.
nodes in max:            ['max2 max 6.0', 'max max2 7.0', 'max max2 9.0', 'max2 max 8.0', 'max2 max 10.0', 'max2 max 11.0']
nodes in max2:           ['max2 max 6.0', 'max max2 7.0', 'max2 max 8.0', 'max max2 9.0', 'max2 max 10.0', 'max2 max 11.0']
current blockchain:      ['0$#$#system system 0.0$#$#0', '6828ce56d978f07d7374fecbcb49ead6defe63a1016e9b89fcead171d7c97808$#$#max max2 1.0$#$#max2 max 2.0$#$#max max2 3.0$#$#max2 max 4.0$#$#max max2 5.0$#$#system max2 1.0$#$#12202259370478495191']

[max2]  I just mined a new block  0000006c94b4be1a4ce7621bea5b8ffcd6c4732363d51f2f42dde7baf108afe0 8428859
wallets: {'system': -2.0, 'max': 1005.0, 'max2': 997.0}
[max]   I'm accepting the new block as it is building on what I already have.
nodes in max:            ['max2 max 11.0']
nodes in max2:           ['max2 max 11.0']
current blockchain:      ['0$#$#system system 0.0$#$#0', '6828ce56d978f07d7374fecbcb49ead6defe63a1016e9b89fcead171d7c97808$#$#max max2 1.0$#$#max2 max 2.0$#$#max max2 3.0$#$#max2 max 4.0$#$#max max2 5.0$#$#system max2 1.0$#$#12202259370478495191', '0000001d970e440955f0a91b64b3e771663decc68e98acba4e9644874c491c80$#$#max2 max 6.0$#$#max max2 7.0$#$#max2 max 8.0$#$#max max2 9.0$#$#max2 max 10.0$#$#system max2 1.0$#$#5319397853656594559']
'''