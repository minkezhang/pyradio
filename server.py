from radio import Radio, q
from threading import Thread
from misc import error

rad = Radio(q)

# the radio streams in background
Thread(target = rad.stream).start()

from os import pipe
rad.add(('127.0.0.1', '50010'), pipe())
rad.add(('127.0.0.1', '50011'), pipe())

def tmp(client):
	(r, w) = rad.reference(client)
	while(True):
		print(r.read(128 * 1024))

tmp(('127.0.0.1', '50010'))

# pipe method
# from os import pipe			# ignore
# (e, w) = pipe()			# ignore
# r.PIPE = (e, w)			# ignore
# (a, b) = pipe()			# ignore
# r.PIPE2 = (a, b)			# ignore

# sock method
# Send UDP broadcast packets
## import sys, time
## from socket import *
## s = socket(AF_INET, SOCK_DGRAM)
## s.bind(('', 0))
## s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
## s.setblocking(0)
## r.s = s

# pipe method
# from os import fdopen			# ignore
# rfp = fdopen(e, 'r')			# ignore
# rfp2 = fdopen(a, 'r')			# ignore

## import select
## port = 50000
## buff = 4 * 1024
## s = socket(AF_INET, SOCK_DGRAM)
## s.bind(('<broadcast>', port))
## s.setblocking(0)

## from sys import stderr
## from time import sleep
## while(True):
	## stderr.write('reading from server...\n')
	### msg = s.recv(bufferSize)
	## result = select.select([s],[],[])
	## msg = result[0][0].recv(buff) 
	## print(msg)
	## stderr.write('read data\n')

# pipe method
# data = rfp.read(128 * 1024)
# while(data):
#	print(data)
#	data = rfp.read(128 * 1024)
