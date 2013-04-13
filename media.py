# media definitions
# currently, only supports audio formats

from misc import DEVNULL

from subprocess import Popen, PIPE
from os import fdopen

# custom exceptions
class SeekError(Exception):
	pass

# wrapper to handle broadcasting status messages
class Status():

	def __init__(self, file, msg = None):
		self.file = file
		if(not(msg)):
			self.msg = Status.time()
		else:
			# slows down message replay
			self.msg = ',, '.join(msg.split(' '))
		self.save()

	# returns a time status
	@staticmethod
	def time():
		from time import localtime, strftime
		base = 'time, announcement,,, it,, is,, now,,'
		h = str(int(strftime('%I', localtime())))
		m = str(int(strftime('%M', localtime())))
		if(int(m) < 10):
			m = 'o, %s' % (m)
		# half-day (AM, PM)
		d = '.'.join(list(strftime('%p', localtime())))
		return('%s %s; %s; %s.' % (base, h, m, d))

	# saves audio file to a temporary file
	def save(self):
		echo = Popen([ 'echo', self.msg ], stdout = PIPE)
		echo.wait()
		espeak = Popen([ 'espeak', '-p', '20', '--stdout' ], stdout = PIPE, stdin = PIPE, stderr = DEVNULL)
		(stdout, stderr) = espeak.communicate(input = echo.stdout.read())
		fp = open(self.file, 'w')
		fp.write(stdout)
		fp.close()

	def delete(self):
		from os import remove
		remove(self.file)

class Media():

	def __init__(self, file):
		self.file = file
		self.duration = 0
		self.tags = {
			'title' : None,
			'artist' : None,
			'album' : None }
		call = Popen([ 'ffmpeg', '-i', file ], stderr = PIPE)
		call.wait()
		
		info = [ str(line).strip() for line in call.stderr.readlines() ]
		# crude info extraction method
		for line in info:
			pass
			# element.strip will probably need to strip inconvenient symbols from the metadata
			formatted = [ element.strip() for element in str(line).split(' :') ]
			if(formatted[0] in [ 'album', 'artist', 'title' ]):
				self.tags[formatted[0]] = formatted[1]
			else:
				# get duration
				formatted = [ element.strip() for element in line.split(', ') ]
				if(formatted[0][0:8] == 'Duration'):
					(hours, minutes, seconds) = [ float(element) for element in formatted[0].split(': ')[1].split(':') ]
					self.duration = hours * 60 * 60 + minutes * 60 + seconds

	def __str__(self):
		# artist / album metadata is song (vs. video) specific
		# this may need to be changed in the future for video support
		return('%s -- %s (%s) : %s' % (self.tags['title'], self.tags['artist'], self.tags['album'], self.duration))

	# tests if file exists
	def exist(self):
		with open(self.file):
			pass

	# sets up ffmpeg to start encoding the media
	# returns the subprocess object (for controlling termination)
	def play(self, pipe, offset = 0):
		(r, w) = pipe

		if(not(self.duration) or (offset >= self.duration)):
			raise SeekError

		offset = max([ 0, offset ])
		# -re arg (real-time encoding support) gives buffer underrun errors
		#
		# directing ffmpeg to stdout
		#	http://bit.ly/ZDIO6B
		# seeking with ffmpeg
		#	http://bit.ly/Tv0mMP
		call = Popen([ 'ffmpeg', '-ss', str(offset), '-re', '-i', self.file, '-f', 'mp3', '-' ], stderr = DEVNULL, stdout = fdopen(w, 'w'))
		return(call)
