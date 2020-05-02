from .handle_share_link import handle_link

def do_link(args):
    show_json = args.show_json
    save = args.save
    for link in args.rest:
        handle_link(link, show_json=show_json, save=save)
