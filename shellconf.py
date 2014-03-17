#!/usr/bin/env python

import subprocess, os
import servers

class ShellConf():


    def __init__(self, shell, scripts):
        self.shell = shell
        self.scripts = scripts

    def log(self):
        pass

    def run(self):
        for server in servers.servers:
            print('------------------------------------------------------------------')
            print('RUNNING SCRIPTS @ ' + server)
            print('------------------------------------------------------------------')

            for fn in os.listdir(self.scripts):
                print('- RUNNING SCRIPT ' + self.scripts + fn + ' @ ' + server + ':')
                subprocess.call('ssh ' + server + ' "' + self.shell + ' -s" < ' + self.scripts + fn, shell=True)
                print('')

            print('')

if __name__ == '__main__':
    sc = ShellConf('bash', './scripts/')
    sc.run()
