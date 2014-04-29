#!/usr/bin/python -W ignore::DeprecationWarning

try:
	import sys
	from lib.version import *
	from lib.main import Main
	from lib.version import *
	from lib.common import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)



def sees():
	main = Main()
	
	while True:
		print >> sys.stdout, bcolors.FAIL + disclamer + bcolors.ENDC
		agree = raw_input()	
		if (agree == "Y" or agree == "y"):
			try:
				try:	
					main.run()
				except Exception, mess:
					print mess
					sys.exit(2)
			except KeyboardInterrupt:
				print message
				sys.exit(3)
		elif (agree == "N" or agree == "n"):
			print message
			sys.exit(4)
		else:
			print wrong_option



if __name__ == "__main__":
	"""
		Main Block for Sees
	"""

	sees()
