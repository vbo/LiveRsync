import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(file('config.example.ini'))

with file('/tmp/LiveRsync.pid', 'w') as pidFile:
    pidFile.write(str(os.getpid()))

while True:
    for folder in config.sections():
        source = config.get(folder, 'source')
        dest = config.get(folder, 'dest')
        command = 'rsync -rlptz -e ssh --out-format="[%t] %o:%f" --delete '  + source + ' ' + dest;
        os.system(command)
        
