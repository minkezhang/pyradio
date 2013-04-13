from radio import Radio, q

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SocketServer

class Server(SocketServer.ThreadingMixIn, HTTPServer):
# class Server(SocketServer.ThreadingMixIn, HTTPServer):
	def __init__(self):
		from threading import Thread

		self.host = 'localhost'
		self.port = 8080

		# create a server with custom handler binding
                SocketServer.TCPServer.__init__(self, (self.host, self.port), RequestHandler)

		self.radio = Radio(q)
		Thread(target = self.radio.stream).start()

	# add a client to the radio client list
	# client is in the form of a (host, port) tuple
	def add(self, client):
		# associates a pipe to a particular client
		# radio.broadcast() will stream to all pipes, which can be accessed from the request handler
		self.radio.add(client)

	# returns the associated pipe to the client
	def reference(self, client):
		return(self.radio.reference(client))

class RequestHandler(SocketServer.StreamRequestHandler):#, BaseHTTPRequestHandler):

	def handle(self):
		self.server.add(self.client_address)
		SocketServer.StreamRequestHandler.handle(self)
		# BaseHTTPRequestHandler.handle(self)

#	def do_GET(self):
#		self.send_response(200)
#		self.send_header('Content-Type', 'audio/mpeg')
#		self.end_headers()

		try:
			(r, w) = self.server.reference(self.client_address)
			data = r.read(128 * 1024)
			while(data):
				self.wfile.write(data)
				self.wfile.flush()
				data = r.read(128 * 1024)
		except IOError:
			pass

		return()

if(__name__ == '__main__'):
	Server().serve_forever()
#	try:
#		a.serve_forever()
#	except KeyboardInterrupt:
#		a.shutdown()
