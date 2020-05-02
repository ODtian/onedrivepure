from O365 import Account, FileSystemTokenBackend
from static import default_client, default_redirect_url
from handle_session import save_session
import os
import time


def init_business(args):
    if args.client_id and args.client_secret and args.redirect_url:
        credentials = (
            args.client_id,
            args.client_secret
        )
        redirect_url = args.redirect_url
    elif args.clients:
        client = args.clients[args.app]
        credentials = (
            client.get('client_id'),
            client.get('client_secret')
        )
        redirect_url = client.get('redirect_uri')
    else:
        credentials = default_client
        redirect_url = default_redirect_url

    save_dir = args.save_dir
    token_backend = FileSystemTokenBackend(
        token_path=save_dir, token_filename=str(int(time.time()))+'_token.json')
    account = Account(credentials)

    account.authenticate(
        scopes=['basic', 'onedrive_all', 'sharepoint_dl'],
        redirect_url=redirect_url,
        token_backend=token_backend
    )
    # save_dir = './ODtoken'

    save_name = account.get_current_user()

    save_path = os.path.join(save_dir, save_name+'.json')
    save_session(account, path=save_path)
    return account
