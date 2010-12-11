#!/usr/bin/env python

import argparse
import LiveRsync

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=LiveRsync.__doc__)
    parser.add_argument('--version', action='version',
                        version='{0} {1}'.format(LiveRsync.PROG, LiveRsync.VERSION))
    group = parser.add_mutually_exclusive_group()
    controller = LiveRsync.Controller()
    for field in dir(controller):
        action = getattr(controller, field)
        if callable(action) and not field.startswith('_'):
            group.add_argument('--{0}'.format(field), '-{0}'.format(field[:1]), action='store_const',
                               const=action, dest='action', help=action.__doc__)
    args = parser.parse_args()
    try:
        args.action()
    except TypeError:
        parser.print_usage()