LiveRsync is very simple real time directory synchronizer based on rsync.

Basic usage
-----------

    $ vim config.ini                     # You must add config section for every directory you want to sync
    $ ./liversync.py                     # And run it

    $ kill -9 `cat /tmp/LiveRsync.pid`  # And stop it, if needed

If you create, modify or delete file(s) in the directory, listed in config.ini LiveRsync instantly
put your changes in the proper dir at the relevant remote server.

It may be most useful for web development, when you edit scipt at the local machine and run/test script
at the remote. If you use SFTP for this porpose and bind it to <save> event of your editor - LiveRsync is for you.


TODO
----

1. (config) File exclusion
2. (config) Other special options (dry-run etc...)
3. Turn on/turn off scripts