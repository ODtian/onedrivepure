from o365 import Account

def init_business(args):
    credential_conf = args.credential_conf
    credentials = (client_id_business,
                   client_secret_business)
    account = Account(credentials)
    account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint_dl'])

    return account
