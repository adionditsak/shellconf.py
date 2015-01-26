shellconf.py
============

Tiny (2.7K) remote configuration with shell scripts for UNIX/Linux systems.

Run local shell scripts chronologically on defined remote servers (asynchronously for each machine, makes it very fast).

MIT licensed - no restrictions.

##Directory structure
  
    .
    |-- README.md
    |-- log
    |   |-- error.log
    |   `-- output.log
    |-- scripts
    |   |-- passwd.sh
    |   |-- list.sh
    |   `-- uname.sh
    |-- servers.py
    `-- shellconf.py
    
####Explained

* ./log/ contains output.log with output of successfully executed scripts, and error.log with output of scripts which has been executed with failure.
* ./scripts/ contains your shell scripts which will be executed one by one as shellconf.py is running.
* ./config.py contains your servers in a list in user@ip format, what shell to use, scripts dir, and scripts sort.
* ./shellconf.py holds the logic.

##How to use

First of all, define your servers in the list of config.py file, with the following format:

    # servers (user@ip)
    servers = [
      'user@ip-1',
      'user@ip-2',
      'user@ip-3',
    ]
  
Then make sure you got what you need in your scripts folder of shell scripts to execute on your remote servers.

You sort the order for when they should be executed from top to bottom, also in the config.py:

    # scripts sort (executed from top to bottom)
    scripts = [
        'uname.sh',
        'list.sh',
        'passwd.sh',
    ]

Class is initiated with variables of what shell to use and where your shell scripts are located. Here you can write whatever shell you would like to use, eg. sh, bash, zsh, csh or ksh. This is the first thing to define in the config.py file:

    # general
    config = [
        # shell type
        'bash',
        # scripts directory
        './scripts/',
    ]

Then use the run() function to run the scripts at your remote servers defined in the config.py list.

    sc.run_for_all_servers() # or sc.run_for_one_server('user@ip')
  
You can call it directly from shellconf.py or run it as a module. 

####As a module from the Python prompt:

    >>> import shellconf
    >>> sc = shellconf.ShellConf(config.config[0], config.config[1])
    >>> sc.run_for_all_servers() # or sc.run_for_one_server('user@ip')
  
####As a CLI

Use -a for configuring all servers, and -s [server-name] for one server.
  
    $ ./shellconf.py -a

or

    $ ./shellconf.py -s user@ip

This will run the shell scripts defined in the config.scripts list, and check if they exist in the scripts directory, on the remote servers.

##Example output
    
    $ python shellconf.py -a
    [RUNNING SCRIPT ./scripts/apt.sh @ root@aarvik.dk]
    [RUNNING SCRIPT ./scripts/apt.sh @ user@ip-2]
    !!! - ERRORS with apt.sh at user@ip-2. See ./log/shellconf.log for details.
    [RUNNING SCRIPT ./scripts/uname.sh @ user@ip-2]
    !!! - ERRORS with uname.sh at user@ip-2. See ./log/shellconf.log for details.
    [RUNNING SCRIPT ./scripts/list.sh @ user@ip-2]
    !!! - ERRORS with list.sh at user@ip-2. See ./log/shellconf.log for details.
    ~~~~~~~ scripts for user@ip-2 completed ~~~~~~~
    *** - SUCCESS with apt.sh at root@aarvik.dk. See ./log/shellconf.log for details.
    [RUNNING SCRIPT ./scripts/uname.sh @ root@aarvik.dk]
    *** - SUCCESS with uname.sh at root@aarvik.dk. See ./log/shellconf.log for details.
    [RUNNING SCRIPT ./scripts/list.sh @ root@aarvik.dk]
    *** - SUCCESS with list.sh at root@aarvik.dk. See ./log/shellconf.log for details.
    ~~~~~~~ scripts for root@aarvik.dk completed ~~~~~~~

##Example ./log/output.log

    ...
    [uname.sh @ user@ip-1] (26/01/2015 | 10:08:17):
    Linux hostname-1 2.6.32-358.2.1.el6.x86_64 #1 SMP Wed Mar 13 00:26:49 UTC 2013 x86_64 x86    _64 x86_64 GNU/Linux
  
    [uname.sh @ user@ip-2] (26/01/2015 | 10:08:17):
    Linux hostname-2 2.6.18-308.4.1.el5 #1 SMP Tue Apr 17 17:08:00 EDT 2012 x86_64 x86_64 x86_64     GNU/Linux
    ...
