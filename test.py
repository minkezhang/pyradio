def client():
	import socket
	import struct

	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((MCAST_GRP, MCAST_PORT))
	mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	while True:
		print sock.recv(10240)

def server():

	import socket

	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

	while True:
		sock.sendto("robot", (MCAST_GRP, MCAST_PORT))

from threading import Thread

s = Thread(target = server)
c = Thread(target = client)

s.daemon = True
c.daemon = True

c.start()
s.start()

c.run()
s.run()
