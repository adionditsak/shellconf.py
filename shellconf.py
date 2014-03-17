#!/usr/bin/env python

import subprocess, os
import servers

class ShellConf():

    def __init__():
        pass

    def run():

        for server in servers.servers:
            print('----------------------------------------------')
            print('Running configuration scripts for: ' + server)
            print('----------------------------------------------')

            for fn in os.listdir('./scripts/'):
                print('--------------- Running script: ' + fn + ' ---------------')
                subprocess.call('ssh ' + server + ' "bash -s" < ./scripts/' + fn, shell=True)
                print('')

            print('')

if __name__ == '__main__':
    ShellConf.run()
