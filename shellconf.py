#!/usr/bin/env python

import sys, subprocess, os, time, threading
import servers


class ShellConf():

    def __init__(self, shell, scripts):
        self.shell = shell
        self.scripts = scripts

    def initiate_server_configuration(self, server):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(server)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('')

        threading.Thread(target=self.run_shell_scripts(server)).start()

    def completed_server_configuration(self, server):
        print('--- ' + server + ' completed ---\n')

    def run_for_all_servers(self):
        for server in servers.servers:
            self.initiate_server_configuration(server)

    def run_for_one_server(self, server):
        self.initiate_server_configuration(server)

    def list_servers(self):
        i = 0
        print('Servers listed (./servers.py):')
        for server in servers.servers:
            print(str(i) + ': ' + server)
            i = i + 1

    def log(self, server, script, log_input):
        with open('./log/shellconf.log', 'a') as log_file:
            log_file.write('[' + script + ' @ ' + server + '] (' + time.strftime("%d/%m/%Y | %H:%M:%S") + '):\n' + str(log_input) + '\n')

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

    def help(self):
        print('Use -a/--all for all servers or -s/--server [server] for one server.')

if __name__ == '__main__':
    sc = ShellConf('bash', './scripts/')

    if len(sys.argv) > 1:
        if sys.argv[1] == '--all' or sys.argv[1] == '-a':
            sc.run_for_all_servers()
        elif sys.argv[1] == '--server' or sys.argv[1] == '-s':
            if len(sys.argv) > 2:
                sc.run_for_one_server(sys.argv[2])
            else:
                sc.help()
                sc.list_servers()
    else:
        sc.help()
