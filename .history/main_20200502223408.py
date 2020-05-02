from onedrivepure.account import do_init
from onedrivepure.share_link import parse_args
from onedrivepure.utils.session import *
from onedrivepure.utils.static import *
from onedrivepure.utils.uploader import *
from onedrivepure.utils.helper_print import *
from onedrivepure.utils.helper_item import *
from onedrivepure.utils.helper_file import *


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
