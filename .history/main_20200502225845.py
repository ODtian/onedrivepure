from onedrivepure.account import do_init, load_session
from onedrivepure.share_link import do_link
from onedrivepure.upload import do_upload
from onedrivepure.args import parse_args
import os

def main():
    args = parse_args()
    if args.mode == 'init':
        client = do_init(args)
        return client
    else:
        client = load_session(path=args.)
    
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
