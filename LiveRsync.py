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
import re


class Config:
    rsh = 'ssh -q -o PasswordAuthentication=no -i {id}'
    baseCommand = "rsync -rlptzq -e '{rsh}' --delete"
    workingDir = os.path.expanduser('~/.liversync/')
    pidFileName = 'pidfile.pid'
    projectsFileName = 'projects.ini'
    excludeSeparator = ' | '


class Warning (Exception):
    pass


class SyncProcess:
    def __init__(self, command):
        self.__command = command
        self.__process = None

    def run(self):
        self.__process = subprocess.Popen(self.__command, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        return self
    
    def wait(self):
        if not self.__process:
            self.run()
        return self.__process.wait()


class Synchronizer:
    def __init__(self):
        self.projects = {}
        self.prepareCommands()

    def prepareCommands(self):
        projectsConf = ConfigParser()
        path = Config.workingDir + Config.projectsFileName        
        try:
            projectsConf.readfp(file(path))
        except IOError:
            raise Warning('No such file {0}'.format(path))        
        for projectName in projectsConf.sections():
            project = {}            
            for k, v in projectsConf.items(projectName):
                project[k] = v            
            rsh = Config.rsh.format(id=project['id'])
            command = Config.baseCommand.format(rsh=rsh)
            if project.has_key('exclude'):
                for exclude in project['exclude'].split(Config.excludeSeparator):
                    command += ' --exclude ' + exclude
            source = project['source']
            dest = project['dest']
            project['command'] = '{0} {1} {2}'.format(command, source, dest)
            self.projects[projectName] = project;

    def syncAll(self):
        for project, params in self.projects.items():
            yield project, params, SyncProcess(params['command'])
            
    def loop(self):
        while True:
            processes = []
            for project, params, process in self.syncAll():
                processes.append(process.run())
            self._wait(processes)

    def _wait(self, processes):
        for process in processes:
            process.wait()


class Controller:
    def __getAddedIds(self):
        ids = []
        command = 'ssh-add -l'
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        p.wait()
        for line in p.stdout:
            matched = re.match(r'''
                (?P<length>\d+)\s
                (?P<fingerprint>.*?)\s
                (?P<path>.+)\s
                \(
                    (?P<type>.*)
                \)$''', line, re.VERBOSE)
            if matched: ids.append(matched.group('path'))
        return ids

    def start(self):
        if self.__getPid():
            print "Seems allready running or killed manually"
            exit();        
        print "Preparing projects."
        try:
            try:
                errors = 0
                addedIds = self.__getAddedIds()
                for project, params, process in Synchronizer().syncAll():
                    if params['id'] not in addedIds:
                        id = os.path.expanduser(params['id'])
                        if id not in addedIds:
                            subprocess.Popen('ssh-add ' + id, shell=True).wait()
                            addedIds.append(id)
                    print 'Checking {0!r}...'.format(project),
                    sys.stdout.flush()
                    result = process.wait()
                    errors += result
                    if result == 0: print 'Ok'
                    else: print 'Error'
                if errors:
                    raise Warning('There were some errors.\n' +
                    'Check out your {dir} and try again'.format(
                        dir=Config.workingDir + Config.projectsFileName))
            except KeyboardInterrupt:
                raise Warning()            
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

        
