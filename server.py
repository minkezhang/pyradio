from radio import Radio, q
from threading import Thread

# pipe method
from os import pipe
r = Radio(q)

(e, w) = pipe()
r.PIPE = (e, w)
(a, b) = pipe()
r.PIPE2 = (a, b)

# sock method
# Send UDP broadcast packets
MYPORT = 50000
import sys, time
from socket import *
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.setblocking(0)

r.s = s

# t runs in background
t = Thread(target = r.stream)
t.start()

# pipe method
from os import fdopen
rfp = fdopen(e, 'r')
rfp2 = fdopen(a, 'r')

import select
port = 50000  # where do you expect to get a msg?
bufferSize = 128 * 1024 # whatever you need

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('<broadcast>', port))
s.setblocking(0)

while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize) 
    print msg


#data = rfp.read(128 * 1024)
#while(data):
#	print(data)
#	data = rfp.read(128 * 1024)
