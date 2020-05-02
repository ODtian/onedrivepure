import time

from O365 import Account, FileSystemTokenBackend

from .handle_session import save_session
from .static import default_client, default_redirect_url


def init_business(args):
    if args.client_id and args.client_secret and args.redirect_url:
        credentials = (
            args.client_id,
            args.client_secret
        )
        redirect_url = args.redirect_url
    elif hasattr(args, 'clients'):
        client = args.clients[args.app]
        credentials = (
            client.get('client_id'),
            client.get('client_secret')
        )
        redirect_url = client.get('redirect_url')
        args.save_account
    else:
        credentials = default_client
        redirect_url = default_redirect_url

    save_dir = args.save_dir
    token_backend = FileSystemTokenBackend(
        token_path=save_dir,
        token_filename=str(int(time.time()))+'_token.json'
    )
    account = Account(credentials, token_backend=token_backend)

    account.authenticate(
        scopes=['basic', 'onedrive_all', 'sharepoint_dl'],
        redirect_uri=redirect_url,
        # notice!!! redirect_uri(i) not l !!!
    )
    save_name
    save_session(account, args)
    return account
