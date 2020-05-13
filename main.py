from onedrivepure.account import do_init
from onedrivepure.share_link import do_link
from onedrivepure.upload import do_upload
from onedrivepure.args import parse_args


def main():
    args = parse_args()
    client = do_init(args, init=(args.mode == "init"))

    if args.mode == "upload":
        do_upload(client, args)

    elif args.mode == "link":
        do_link(args)
    # elif args.mode == 'put':
    #     do_put(client, args)

    # elif args.mode == 'share':
    #     do_share(client, args)

    # elif args.mode == 'direct':
    #     do_direct(client, args)

    # elif args.mode == 'delete':
    #     do_delete(client, args)

    # elif args.mode == 'mkdir':
    #     do_mkdir(client, args)

    # elif args.mode == 'move':
    #     do_move(client, args)

    # elif args.mode == 'remote':
    #     do_remote(client, args)

    # elif args.mode == 'search':
    #     do_search(client, args)

    # elif args.mode == 'quota':
    #     do_quota(client, args)


if __name__ == "__main__":
    main()
