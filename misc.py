# Ubuntu 12.10
# sudo apt-get install ffmpeg libavcodec-extra-53
# sudo apt-get install espeak

from subprocess import Popen

DEVNULL = open('/dev/null', 'w')

def pkg(program, package):
	return('\'%s\' (in pkg \'%s\') is not installed' % (program, package))

def installed(program, package = None):
	if(not(package)):
		package = program
	try:
		Popen([ program ], stderr = DEVNULL, stdout = DEVNULL)
	except OSError:
		error(pkg(program, package))
		return(False)
	return(True)

def error(msg):
	from sys import stderr
	stderr.write('error: %s\n' % (msg))
