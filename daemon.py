#!/usr/bin/env python

import os
from ConfigParser import ConfigParser
import subprocess

import config

class LiveRsync:
    def __init__(self):
        self.commands = {}       
        self.prepareCommands()

    def prepareCommands(self):
        projects = ConfigParser()
        try:
            projects.readfp(file(config.workingDir + config.projectsFileName))
            for project in projects.sections():
                source = projects.get(project, 'source')
                dest = projects.get(project, 'dest')
                self.commands[project] = ' '.join((config.baseCommand, source, dest))
        except IOError:
            print 'Please, create', config.workingDir, 'and use', config.projectsFileName, 'for configure LiveRsync'
            exit()

    def mainLoop(self):
        while True:
            for project, command in self.commands.items():
                os.system(command)        

if __name__ == '__main__':
    LiveRsync().mainLoop()

        
