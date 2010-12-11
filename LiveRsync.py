#!/usr/bin/env python

from ConfigParser import ConfigParser
import subprocess

import config

class Daemon:
    def __init__(self):
        self.commands = {}
        self.prepareCommands()

    def prepareCommands(self):
        projects = ConfigParser()
        projects.readfp(file(config.workingDir + config.projectsFileName))
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

if __name__ == '__main__':
    Daemon().mainLoop()

        
