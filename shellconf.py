#!/usr/bin/env python

import sys, subprocess, os, time, threading
import servers


class ShellConf():

    def __init__(self, shell, scripts):
        self.shell = shell
        self.scripts = scripts
        self.lock = threading.Lock()
        
        
    def run_for_all_servers(self):
        for server in servers.servers:
            threading.Thread(target=lambda:self.run_shell_scripts(server)).start() # async

    def run_for_one_server(self, server):
        self.run_shell_scripts(server)

    def list_servers(self):
        print('Servers listed (./servers.py):')
        for i, server in enumerate(servers.servers):
            print(str(i) + ': ' + server)

    def log(self, server, script, log_input):
        with self.lock, open('./log/shellconf.log', 'a') as log_file:
            log_file.write('[%s @ %s] (%s):\n%s\n\n' % (script, server, time.strftime("%d/%m/%Y | %H:%M:%S"), log_input))

    def run_shell_scripts(self, server):
        with self.lock:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(server)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('')

        for fn in os.listdir(self.scripts):
            with self.lock:
                print('[RUNNING SCRIPT ' + self.scripts + fn + ' @ ' + server + ']')

            cmd = 'ssh ' + server + ' "' + self.shell + ' -s" < ' + self.scripts + fn
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, errors = p.communicate()

            if p.returncode:
                self.log(server, fn, errors)
                with self.lock:
                    print('- ERRORS. See ./log/shellconf.log for details.\n')
            else:
                self.log(server, fn, output)
                with self.lock:
                    print('- SUCCESS. See ./log/shellconf.log for details.\n')
        with self.lock:
            print('--- ' + server + ' completed ---\n')

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
