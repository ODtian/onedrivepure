from O365 import Account
from static import default_client, default_redirect_url
from handle_session import save_session


def init_business(args):
    if args.client_id and args.client_secret and args.redirect_uri:
        credentials = (
            args.client_id,
            args.client_secret
        )
        redirect_uri = args.redirect_url
    elif args.clients:
        client = args.clients[args.app]
        credentials = (
            client.get('client_id'),
            client.get('client_secret')
        )
        redirect_ur; = client.get('redirect_uri')
    else:
        credentials = default_client
        redirect_url = default_redirct_url
    account = Account(credentials)
    account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint_dl'])
    save_path = './'+account.get_current_user()+'.json'
    return account
