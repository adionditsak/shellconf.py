#!/usr/bin/env python

import subprocess, os, time, threading
import servers


class ShellConf():

    def __init__(self, shell, scripts):
        self.shell = shell
        self.scripts = scripts

    def run(self):
        for server in servers.servers:
            t = threading.Thread(target=self.run_shell_scripts(server))
            t.start()

    def log(self, server, script, log_input):
        with open('./log/shellconf.log', 'a') as log_file:
            log_file.write('[' + script + ' @ ' + server + '] (' + time.strftime("%H:%M:%S - %d/%m/%Y") + '):\n' + log_input + '\n')

    def run_shell_scripts(self, server):
        for fn in os.listdir(self.scripts):
            print('[RUNNING SCRIPT ' + self.scripts + fn + ' @ ' + server + ']')

            cmd = 'ssh ' + server + ' "' + self.shell + ' -s" < ' + self.scripts + fn

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            output, errors = p.communicate()

            if p.returncode:
                self.log(server, fn, errors)
                print('- SCRIPT HAS BEEN EXECUTED WITH ERRORS, SEE MORE AT ./log/shellconf.log.')
            else:
                self.log(server, fn, output)
                print('- SCRIPT HAS BEEN EXECUTED WITH SUCCESS, SEE MORE AT ./log/shellconf.log.')


if __name__ == '__main__':
    sc = ShellConf('bash', './scripts/')
    sc.run()
