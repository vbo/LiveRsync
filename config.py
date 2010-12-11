"""LiveRsync configuration module"""

import os.path

_rsh = 'ssh -q -o PasswordAuthentication=no'
baseCommand = "rsync -rlptzq -e '%s' --delete" % _rsh

workingDir = os.path.expanduser('~/.liversync/')
pidFileName = 'pidfile.pid'
projectsFileName = 'projects.ini'