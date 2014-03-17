#!/usr/bin/env python

import subprocess
import servers

for server in servers.servers:
    subprocess.call('ssh ' + server + ' "bash -s" < ./scripts/list.sh', shell=True)
