#!/usr/bin/env python

""" import default modules """
import subprocess, os

""" get servers """
import servers

for server in servers.servers:
    print('----------------------------------------------')
    print('Running configuration scripts for: ' + server)
    print('----------------------------------------------')

    for fn in os.listdir('./scripts/'):
        print('--------------- Running script: ' + fn + ' ---------------')
        subprocess.call('ssh ' + server + ' "bash -s" < ./scripts/' + fn, shell=True)
        print('')

    print('')
