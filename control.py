#!/usr/bin/env python

import os
import sys
import subprocess
import signal
import shutil

import config
import LiveRsync

toolName = 'LiveRsync'

def doStart():    
    if getPid():
        print "Seems allready running or killed manually"
        exit();

    errors = 0
    print "Checking projects. Be patient..."
    for project, process in LiveRsync.Daemon().syncAll():
        print '{0!r:<15}\t'.format(project),
        result = process.wait()
        errors += result
        if result == 0:
            print 'Ok'
        else:
            print 'Error'
        
    if errors:
        print 'There were some errors.'
        print 'Check out your {dir} and try again'.format(dir=config.workingDir + config.projectsFileName);
        exit();

    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    pid = subprocess.Popen(os.path.join(dir, 'LiveRsync.py')).pid
    createPidFile(pid)
    print "{0} started with pid {1}".format(toolName, pid)
        

def doStop():
    pid = getPid()
    if pid:
        try:
            os.kill(pid, signal.SIGKILL)
            print "{0} process (pid {1}) successfully killed".format(toolName, pid)
        except OSError:
            print "Seems allready killed"
        deletePidFile()
    else:
        print 'Seems not running'

def doInstall():
    try:
        os.makedirs(config.workingDir)
        shutil.copyfile('projects-example.ini', config.workingDir + config.projectsFileName)
        print '{0} installed'.format(toolName)
    except OSError:
        print "Seems already installed. Remove {0} to uninstall".format(config.workingDir)

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

