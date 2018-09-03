import sys
if sys.version_info[0]<3:
	raise Exception("python3 required! current (wrong) version: '%s'" % sys.version_info)

sys.path.insert(0,'/home/rhfktj/gosit/server/')
from route import app as application
