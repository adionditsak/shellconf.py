#!/usr/bin/env python

"""
shellconf.py - Simple remote configuration with shell for UNIX/Linux systems.

:copyright: (c) 2014 Anders Aarvik
:author: Anders Aarvik (aarvik92@gmail.com) and contributors
:license: MIT licensed. See LICENSE.txt

Requirements
* You need an authorized ssh public key on remote servers for shellconf.py to be functional
"""

import sys
import subprocess
import os
import time
import threading

import config


class ShellConf():

    def __init__(self, shell, scripts):
        self.shell = shell
        self.scripts = scripts
        self.lock = threading.Lock()

    def run_for_all_servers(self):
        for server in config.servers:
            threading.Thread(target=lambda: self.run_shell_scripts(server)).start() # async

    def run_for_one_server(self, server):
        self.run_shell_scripts(server)

    def list_servers(self):
        print('Servers listed (./servers.py):')
        for i, server in enumerate(config.servers):
            print('%s: %s' % (str(i), server))

    def log(self, server, script, log_input, log_type):
        if log_type == 'error':
            log = './log/error.log'
        elif log_type == 'success':
            log = './log/output.log'

        with self.lock, open(log, 'a') as log_file:
            log_file.write('[%s @ %s] (%s):\n%s\n\n' % (script, server, time.strftime("%d/%m/%Y | %H:%M:%S"), log_input))

    def run_shell_scripts(self, server):
        for fn in config.scripts:
            if os.path.isfile(self.scripts + fn):
                with self.lock:
                    print('[RUNNING SCRIPT %s%s @ %s]' % (self.scripts, fn, server))

                cmd = 'ssh %s "%s -s" < %s%s' % (server, self.shell, self.scripts, fn)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, errors = p.communicate()

                if p.returncode:
                    self.log(server, fn, errors, 'error')
                    with self.lock:
                        print('!!! - ERRORS with %s at %s. See ./log/error.log for details.' % (fn, server))
                else:
                    self.log(server, fn, output, 'success')
                    with self.lock:
                        print('*** - SUCCESS with %s at %s. See ./log/output.log for details.' % (fn, server))
            else:
                self.log(server, fn, "Script does not exist in scripts directory %s" % self.scripts, 'error')
                with self.lock:
                    print('!!! - SCRIPT %s NOT FOUND in scripts directory %s. See ./log/error.log for details.' % (fn, self.scripts))

        with self.lock:
            print('~~~~~~~ scripts for %s completed ~~~~~~~' % server)

    def help(self):
        print('Use -a/--all for all servers or -s/--server [server] for one server.')

if __name__ == '__main__':
    sc = ShellConf(config.config[0], config.config[1])

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
        sc.list_servers()
