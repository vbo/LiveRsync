#!/usr/bin/env python
"""Real time directory synchronization tool based on rsync"""
PROG = 'LiveRsync'
VERSION = 0.42

from ConfigParser import ConfigParser
import subprocess
import os
import sys
import signal
import shutil

class Config:
    __rsh = 'ssh -q -o PasswordAuthentication=no'
    baseCommand = "rsync -rlptzq -e '%s' --delete" % __rsh
    workingDir = os.path.expanduser('~/.liversync/')
    pidFileName = 'pidfile.pid'
    projectsFileName = 'projects.ini'

class Synchronizer:
    def __init__(self):
        self.commands = {}
        self.prepareCommands()

    def prepareCommands(self):
        projects = ConfigParser()
        path = Config.workingDir + Config.projectsFileName
        try:
            projects.readfp(file(path))
        except IOError:
            raise Warning('No such file {0}'.format(path))
        
        for project in projects.sections():
            source = projects.get(project, 'source')
            dest = projects.get(project, 'dest')
            self.commands[project] = ' '.join((Config.baseCommand, source, dest))

    def syncAll(self):
        for project, command in self.commands.items():
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            yield project, process
            
    def loop(self):
        while True:
            processes = []
            for project, process in self.syncAll():
                processes.append(process)
            self._wait(processes)

    def _wait(self, processes):
        for process in processes:
            process.wait()

class Warning (Exception):
    pass

class Controller:
    def start(self):
        if self.__getPid():
            print "Seems allready running or killed manually"
            exit();

        errors = 0
        print "Checking projects. Be patient..."
        try:
            for project, process in Synchronizer().syncAll():
                print '{0!r:<15}\t'.format(project),
                result = process.wait()
                errors += result
                if result == 0:
                    print 'Ok'
                else:
                    print 'Error'
            if errors:
                raise Warning('There were some errors.\n' +
                'Check out your {dir} and try again'.format(
                    dir=Config.workingDir + Config.projectsFileName))
        except Warning as e:
            print e
            exit()

        dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        pid = subprocess.Popen(os.path.join(dir, 'LiveRsync.py')).pid
        self.__createPidFile(pid)
        print "LiveRsync daemon started with pid", pid


    def kill(self):
        pid = self.__getPid()
        if pid:
            try:
                os.kill(pid, signal.SIGKILL)
                print "{0} daemon (pid {1}) successfully killed".format(PROG, pid)
            except OSError:
                print "Seems allready killed"
            self.__deletePidFile()
        else:
            print 'Seems not running'

    def install(self):
        try:
            os.makedirs(Config.workingDir)
            shutil.copyfile('projects-example.ini', Config.workingDir + Config.projectsFileName)
            print 'LiveRsync successfully installed'
        except OSError:
            print "Seems already installed. Remove {0} to uninstall".format(Config.workingDir)

    def restart(self):
        self.kill()
        self.start()

    def __createPidFile(self, pid):
        with file(Config.workingDir + Config.pidFileName, 'w') as pidFile:
            pidFile.write(str(pid))

    def __deletePidFile(self):
        os.remove(Config.workingDir + Config.pidFileName)

    def __getPid(self):
        try:
            f = file(Config.workingDir + Config.pidFileName)
            pid = int(f.readline())
            return pid
        except IOError:
            return False

if __name__ == '__main__':
    Synchronizer().loop()

        
