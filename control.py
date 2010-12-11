#!/usr/bin/env python

import os
import sys
import subprocess
import signal
import shutil
import argparse

import config
import LiveRsync

toolName = 'LiveRsync'
class Controller:    
    def start(self):
        if self.__getPid():
            print "Seems allready running or killed manually"
            exit();

        errors = 0
        print "Checking projects. Be patient..."
        try:
            for project, process in LiveRsync.Daemon().syncAll():
                print '{0!r:<15}\t'.format(project),
                result = process.wait()
                errors += result
                if result == 0:
                    print 'Ok'
                else:
                    print 'Error'
        except LiveRsync.Warning as e:
            print e
            exit()

        if errors:
            print 'There were some errors.'
            print 'Check out your {dir} and try again'.format(dir=config.workingDir + config.projectsFileName);
            exit();

        dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        pid = subprocess.Popen(os.path.join(dir, 'LiveRsync.py')).pid
        self.__createPidFile(pid)
        print "{0} started with pid {1}".format(toolName, pid)
        

    def kill(self):
        pid = self.__getPid()
        if pid:
            try:
                os.kill(pid, signal.SIGKILL)
                print "{0} process (pid {1}) successfully killed".format(toolName, pid)
            except OSError:
                print "Seems allready killed"
            self.__deletePidFile()
        else:
            print 'Seems not running'

    def install(self):
        try:
            os.makedirs(config.workingDir)
            shutil.copyfile('projects-example.ini', config.workingDir + config.projectsFileName)
            print '{0} installed'.format(toolName)
        except OSError:
            print "Seems already installed. Remove {0} to uninstall".format(config.workingDir)

    def restart(self):
        self.kill()
        self.start()

    def __createPidFile(self, pid):
        with file(config.workingDir + config.pidFileName, 'w') as pidFile:
            pidFile.write(str(pid))

    def __deletePidFile(self):
        os.remove(config.workingDir + config.pidFileName)

    def __getPid(self):
        try:
            f = file(os.path.expanduser(config.workingDir + config.pidFileName))
            pid = int(f.readline())
            return pid
        except IOError:
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=LiveRsync.Daemon.__doc__)
    parser.add_argument('--version', action='version', version=LiveRsync.Daemon.VERSION)
    group = parser.add_mutually_exclusive_group()
    controller = Controller()
    for field in dir(controller):
        action = getattr(controller, field)
        if callable(action) and not field.startswith('_'):
            group.add_argument('--{0}'.format(field), '-{0}'.format(field[:1]), action='store_const',
                               const=action, dest='action', help=action.__doc__)
    args = parser.parse_args()
    try:
        args.action()
    except TypeError:
        parser.print_usage()