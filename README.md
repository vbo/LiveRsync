LiveRsync
=========

LiveRsync is a simple tool for Unix systems which provides real time synchronization of your files
and directories with the remote machine. It written in python and based on rsync and ssh.


Installation and basic usage
----------------------------

 * Put sources in the proper folder of your machine (e.g. `~/opt/LiveRsync`).
 * Create alias for LiveRsync control script: `alias liversync='~/opt/LiveRsync/control.py'`.
 * Type `liversync --install` to prepare the working directory and example configuration file.

Now you should `edit ~/.liversync/projects.ini` to add the config section for each directory
(I call it "Project") you want to sync. Type `liversync --start` to start daemon.

Now if you create, modify or delete file(s) in the directory, listed in `projects.ini`,
LiveRsync instantly put your changes in the proper directory at the relevant remote server.
You may stop daemon by typing `liversync --kill`.

I usually use LiveRsync for web development, when I want to edit script sources at the local
machine and run/test script at the remote. Earlier I used SFTP for this porpose and bound uploading
to the SAVE event of my editor. LiveRsync has changed my life for the better =)


Configuration syntax
--------------------

LiveRsync uses only one very simple configuration file - `~/.liversync/projects.ini`.
For each directory you want to sync, you should add a separate project:

    [myProject]
    source=/path/to/myProject/
    dest=me@my.remote.machine:path/on/remote/myProject/
    id=~/.ssh/id_rsa


TODO
----

* File exclusion support in projects.ini
* Other special options support (dry-run etc...)
* Decrease network load on linux (pyinotify)
* Being real daemon (check this out http://www.python.org/dev/peps/pep-3143/)