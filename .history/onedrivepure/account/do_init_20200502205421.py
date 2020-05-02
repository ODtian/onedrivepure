from o365 import Account
from 
import json


def init_business(args):
    if args.clients:
        client = args.clients[args.app]
        args.client_id = client.get('client_id')
        args.client_secret = client.get('client_secret')
    else
    credential_conf = args.credential_conf
    credentials = (client_id_business,
                   client_secret_business)
    account = Account(credentials)
    account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint_dl'])

    return account
