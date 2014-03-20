shellconf.py
============

Simple remote configuration with shell for UNIX/Linux systems.

Run local shell scripts on defined remote servers chronologically.

##Directory structure
  
    .
    |-- README.md
    |-- log
    |   `-- shellconf.log
    |-- scripts
    |   |-- apt.sh
    |   |-- list.sh
    |   `-- uname.sh
    |-- servers.py
    `-- shellconf.py

##How to use

First of all, define your servers in the list of servers.py file, with the following format:

    servers = ['user@ip-1', 'user@ip-2']
  
Then make sure you got what you need in your scripts folder of shell scripts to execute on your remote servers.

Initiate class with arguments of what shell to use and where your shell scripts are located. Here you can write whatever shell you would like to use, eg. sh, bash, zsh, csh or ksh:

    sc = ShellConf('bash', './scripts/')
  
Then use the run() function to run the scripts at your remote servers defined in the servers.py list.

    sc.run()
  
You can call it directly from shellconf.py or run it as a module. 

As a module from the Python prompt:

    >>> import shellconf
    >>> sc = shellconf.ShellConf('bash', './scripts/')
    >>> sc.run()
  
As a CLI:

Use -a for configuring all servers, and -s [server-name] for one server.
  
    $ python shellconf.py -a

or

    $ python shellconf.py -s user@ip

This would run the shell scripts placed in ./scripts/ on the remote servers one by one.
