#!/usr/bin/env python

import os
import sys
import subprocess
import signal
import config

toolName = 'LiveRsync'

def doStart():
    print "Trying to start", toolName
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    if not getPid() or '-f' in sys.argv:
        pid = subprocess.Popen(os.path.join(dir, 'daemon.py')).pid
        createPidFile(pid)
        print "Started with pid", pid
    else:
        print "Seems allready running. Specify -f to start anyway"

def doStop():
    pid = getPid()
    if pid:
        os.kill(pid, signal.SIGKILL)
        deletePidFile()
        print "%s process (pid %d) successfully killed" % (toolName, pid)
    else:
        print 'Seems not running'

def doInstall():
    print 'Trying to create working dir (%s)' % config.workingDir
    try:
        os.makedirs(config.workingDir)
    except OSError:
        print "Seems already exists"

def createPidFile(pid):
    with file(config.workingDir + config.pidFileName, 'w') as pidFile:
        pidFile.write(str(pid))

def deletePidFile():
    os.remove(config.workingDir + config.pidFileName)

def getPid():
    try:
        f = file(os.path.expanduser(config.workingDir + config.pidFileName))
        pid = int(f.readline())
        return pid
    except IOError:
        return False

if __name__ == "__main__":
    toDo = sys.argv[1]
    if toDo == 'install':
        doInstall()
    elif toDo == 'start':
        doStart()
    elif toDo == 'stop':
        doStop()
    elif toDo == 'restart':
        doStop()
        doStart()

