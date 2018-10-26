#!/bin/python

import argparse
import sys
import os
from pypass import Pypass

VERSION = 1.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command to run", choices=['print', 'add', 'version', 'delete'])
    parser.add_argument("-d", help="decrypt password", action="store_true")
    parser.add_argument("-i", help="specify index of record", type=int)
    parser.add_argument("-k", help="specify key of record", type=str)
    parser.add_argument("-c", help="clean terminal", action="store_true")
    parser.add_argument("-u", help="put username into clipboard instead of password", action="store_true")
    parser.add_argument("--masterpass", help="give master password from call", type=str)
    parser.add_argument("--clip", help="paste password to clipboard", action="store_true")
    args = parser.parse_args()
    if args.c:
        os.system('cls' if os.name == 'nt' else 'clear')
    if args.command is None:
        print("No command given...try --help")
        sys.exit(1)
    instance = Pypass(args.masterpass)
    if args.command == 'print':
        if args.clip:
            if args.i is None and args.k is None:
                print('specify record index (option -i) or record key (option -k)')
                sys.exit(1)
            if not args.d:
                print('you must use -d option to decrypt the password')
                sys.exit(1)
            instance.record_to_clipboard(args.i, args.k, args.u)
            sys.exit(0)
        if args.d:
            instance.print(True, args.i, args.k)
        else:
            instance.print(False, args.i, args.k)
    elif args.command == 'add':
        instance.add_record()
    elif args.command == 'version':
        print(' ____        ____               ')
        print('|  _ \ _   _|  _ \ __ _ ___ ___ ')
        print('| |_) | | | | |_) / _` / __/ __|')
        print('|  __/| |_| |  __/ (_| \__ \__ \\')
        print('|_|    \__, |_|   \__,_|___/___/')
        print('       |___/                    ')
        print('version: ' + str(VERSION))
    elif args.command == 'delete':
        if args.i is None:
            print('You have to specify number of record with -i')
            sys.exit(1)
        else:
            instance.delete(int(args.i))
    else:
        print('Unrecognized command, try --help')
        sys.exit(1)

    sys.exit(0)
