"""LiveRsync configuration module"""

import os.path

baseCommand = 'rsync -rlptz -e ssh --out-format="[%t] %o:%f" --delete'
workingDir = os.path.expanduser('~/.liversync/')
pidFileName = 'pidfile.pid'
projectsFileName = 'projects.ini'