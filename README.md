LiveRsync
=========

LiveRsync is a simple tool for Unix systems, which synchronizes your files and directories with remote machine.
It written in python and based on rsync.


Installation and basic usage
------------

 * Put sources in proper folder (ex. `~/opt/LiveRsync`).
 * Create alias for LiveRsync control script this way `alias liversync='~/opt/LiveRsync/control.py'`.
 * Type `liversync install` to prepare working directory and example configuration file.

Now you may `edit ~/.liversync/projects.ini` and add config section for each directory
(I call it "Project") you want to sync. Type `liversync start` to start daemon.

Now, if you create, modify or delete file(s) in the directory, listed in projects.ini,
LiveRsync instantly put your changes in the proper dir at the relevant remote server.
You may stop daemon, typing `liversync stop`.

I usually use LiveRsync for web development, when I want to edit script sources at the local
machine and run/test script at the remote. Earlier I use SFTP for this porpose and bind uploading
to SAVE event of my editor. LiveRsync change my life for the better =)


Error handling
--------------

Nowadays, LiveRsync daemon dies, when rsync returns error code. Usually this means bad connection
or bad `projects.ini` section. If it happens check out error log in `~/.liversync/status.log`


TODO
----

* Improve error handling
* Rewrite hodgie code in control script (argparse)
* File exclusion support in projects.ini
* Other special options support (dry-run etc...)
* Being real daemon (check this out http://www.python.org/dev/peps/pep-3143/)