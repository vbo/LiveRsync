#!/usr/bin/env python

import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(file('config.ini'))

with file('/tmp/LiveRsync.pid', 'w') as pidFile:
    pidFile.write(str(os.getpid()))

while True:
    for directory in config.sections():
        source = config.get(directory, 'source')
        dest = config.get(directory, 'dest')
        command = 'rsync -rlptz -e ssh --out-format="[%t] %o:%f" --delete '  + source + ' ' + dest + ' > /dev/null';
        os.system(command)
        
