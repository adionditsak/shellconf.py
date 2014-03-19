#!/usr/bin/env python

import subprocess, os, time, threading
import servers


class ShellConf():

    def __init__(self, shell, scripts):
        self.shell = shell
        self.scripts = scripts

    def run(self):
        for server in servers.servers:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(server)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('')
            t = threading.Thread(target=self.run_shell_scripts(server))
            t.start()

    def log(self, server, script, log_input):
        with open('./log/shellconf.log', 'a') as log_file:
            log_file.write('[' + script + ' @ ' + server + '] (' + time.strftime("%d/%m/%Y | %H:%M:%S") + '):\n' + log_input + '\n')

    def run_shell_scripts(self, server):
        for fn in os.listdir(self.scripts):
            print('[RUNNING SCRIPT ' + self.scripts + fn + ' @ ' + server + ']')

            cmd = 'ssh ' + server + ' "' + self.shell + ' -s" < ' + self.scripts + fn

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, errors = p.communicate()

            if p.returncode:
                self.log(server, fn, errors)
                print('- ERRORS. See ./log/shellconf.log for details.\n')
            else:
                self.log(server, fn, output)
                print('- SUCCESS. See ./log/shellconf.log for details.\n')


if __name__ == '__main__':
    sc = ShellConf('bash', './scripts/')
    sc.run()
