# Ubuntu 12.10
# sudo apt-get install ffmpeg libavcodec-extra-53
# sudo apt-get install espeak

from media import Status, Media, SeekError
from misc import pkg, installed, error, DEVNULL

from subprocess import Popen, PIPE
from os import fdopen

from collections import deque

class Radio():
	def __init__(self, queue):
		self.start()
		self.queue = deque(queue)

	def enqueue(self, file, offset = 0):
		self.queue.appendleft(file)

	def stream(self):
		from random import random
		while(self.queue):
			if(random() > 0.85):
				self.broadcast(Media(Status('time').file))
				Status('time').delete()
			self.broadcast(Media(self.queue.pop()), title = (random() > 0.75))
		self.stop()

	def start(self):
		if(not(installed('ffmpeg') and installed('espeak'))):
			self.stop()

	def stop(self):
		exit(0)

	def broadcast(self, media, offset = 0, title = False, chunks = 128):
		try:
			media.exist()
		except IOError:
			error('cannot open file, skipping current track')
			return()

		if(title):
			from random import random
			placement = (random() > 0.5)

		if(title and placement):
			try:
				tmp = Status(media.tags['title'], 'the, next, song, is,, %s; by, %s.' % (media.tags['title'], media.tags['artist']))
				self.broadcast(Media(tmp.file))
				tmp.delete()
			except TypeError:
				pass

		# transcodes media
		from os import pipe
		(r, w) = pipe()
		try:
			call = media.play((r, w), offset = offset)
		except SeekError:
			error('illegal seek value, skipping current track')
			return()

		# reads output data to be streamed
		buffer = chunks * 1024
		from os import fdopen
		fp = fdopen(r, 'r')
		try:
			data = fp.read(buffer)
			while(data):
				print(data)
				data = fp.read(buffer)
			call.kill()
			if(title and not(placement)):
				try:
					tmp = Status(media.tags['title'], 'that was %s; by, %s.' % (media.tags['title'], media.tags['artist']))
					self.broadcast(Media(tmp.file))
					tmp.delete()
				except TypeError:
					pass
		except KeyboardInterrupt:
			call.kill()
			# shutdown
			exit(0)
		# IOError occurs when stream is interrupted (i.e. client disconnect)
		except IOError:
			call.kill()
			# shutdown
			exit(0)

if(__name__ == '__main__'):
	q = [
		'/usr/share/sounds/alsa/Front_Center.wav',
		'/usr/share/sounds/alsa/Front_Center.wav',
		'/usr/share/sounds/alsa/Front_Center.wav' ]
	r = Radio(q)
	r.enqueue('/home/mzhang/Downloads/renmd.mp3')
	# endgame: one stream per connection, streams run in background, sync'd queues
	# currently: one stream total, stream runs in foreground
	r.stream()
