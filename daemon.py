#!/usr/bin/env python

from ConfigParser import ConfigParser
import subprocess

import config

class LiveRsync:
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

    def mainLoop(self):
        while True:
            allright = True
            for project, command in self.commands.items():
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if p.wait() != 0:
                    log = file(config.workingDir + config.shortLogFileName, 'w')
                    log.write('Project: ' + project + '\n')
                    for err in p.stderr:
                        log.write(err)
                    log.write('\n')
                    log.close()
                    allright = False
            if not allright:
                exit()

if __name__ == '__main__':
    LiveRsync().mainLoop()

        
