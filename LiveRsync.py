#!/usr/bin/env python

from ConfigParser import ConfigParser
import subprocess

import config

class Daemon:
    """Real time directory synchronization tool based on rsync"""
    VERSION = 'LiveRsync 0.4'
    
    def __init__(self):
        self.commands = {}
        self.prepareCommands()

    def prepareCommands(self):
        projects = ConfigParser()
        path = config.workingDir + config.projectsFileName
        try:
            projects.readfp(file(path))
        except IOError:
            raise Warning('No such file {0}'.format(path))
        
        for project in projects.sections():
            source = projects.get(project, 'source')
            dest = projects.get(project, 'dest')
            self.commands[project] = ' '.join((config.baseCommand, source, dest))
        

    def syncAll(self):
        for project, command in self.commands.items():
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            yield project, process
            
    def mainLoop(self):
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

if __name__ == '__main__':
    Daemon().mainLoop()

        
