#!/usr/bin/env python
# coding:utf-8
# Author:  Beining --<i@cnbeining.com>
# Purpose: A command line client for OneDrive
# Created: 09/23/2016


from onedrivecmd.utils.actions import *
from onedrivecmd.utils.arguments import parse_args
from onedrivecmd.utils.session import *
from onedrivecmd.utils.static import *
from onedrivecmd.utils.uploader import *
from onedrivecmd.utils.helper_print import *
from onedrivecmd.utils.helper_item import *
from onedrivecmd.utils.helper_file import *


def main():
    args = parse_args()
    client = None
    if args.mode == 'init' or args.mode == 'init_business':
        client = do_init(client, args)
        print('Logged in, saving information...')
        save_session(client, path=args.conf)
        return
    client = load_session(path=args.conf)
    if args.mode == 'get':
        do_get(client, args)

    elif args.mode == 'list':
        do_list(client, args)

    elif args.mode == 'put':
        do_put(client, args)

    elif args.mode == 'share':
        do_share(client, args)

    elif args.mode == 'direct':
        do_direct(client, args)

    elif args.mode == 'delete':
        do_delete(client, args)

    elif args.mode == 'mkdir':
        do_mkdir(client, args)

    elif args.mode == 'move':
        do_move(client, args)

    elif args.mode == 'remote':
        do_remote(client, args)

    elif args.mode == 'search':
        do_search(client, args)

    elif args.mode == 'quota':
        do_quota(client, args)


if __name__ == '__main__':
    main()
