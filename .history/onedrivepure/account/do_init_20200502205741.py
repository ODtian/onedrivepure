from o365 import Account
from ..static import default_client
import json


def init_business(args):
    if args.client_id and args.client_secret:
        credentials = (
            args.client_id,
            args.client_secret
        )
    elif args.clients:
        client = args.clients[args.app]
        credentials = (
            client.get('client_id'),
            client.get('client_secret')
        )
        args.client_id =
        args.client_secret =
    else:
        
    credential_conf = args.credential_conf
    = (client_id_business,
       client_secret_business)
    account = Account(credentials)
    account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint_dl'])

    return account
