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
