#!/usr/bin/env python

"""
shellconf.py - Simple remote configuration with shell for UNIX/Linux systems.

:copyright: (c) 2014 Anders Aarvik
:author: Anders Aarvik (aarvik92@gmail.com) and contributors
:license: MIT licensed. See LICENSE.txt

Requirements
* You need an authorized ssh public key on remote servers for shellconf.py to be functional
"""

# general
config = [
    # shell type
    'bash',
    # scripts directory
    './scripts/',
]

# servers (user@ip)
servers = [
  'user@ip-1', 
  'user@ip-2',
  'user@ip-3',
  'user@ip-4',
  'user@ip-5',
]

# scripts sort (executed from top to bottom)
scripts = [
    'uname.sh',
    'list.sh',
    'passwd.sh',
]

