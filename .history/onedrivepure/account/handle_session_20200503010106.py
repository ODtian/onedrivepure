import dill
import os
import types
from .status import default_account_name


def get_save_path(args):
    if not args.save_account_name:
        args.save_account_name = default_account_name
    if args.app:
        args.save_account_name += '_'+str()
    save_path = os.path.join(
        args.save_dir,
        args.save_account_name
    )
    return save_path


def save_session(client, args):
    save_path = get_save_path(args)
    client_saved = dill.dumps(client)
    with open(save_path, 'wb') as f:
        f.write(client_saved)
    return client


def load_session(args):
    save_path = get_save_path(args)
    with open(save_path, 'rb') as f:
        client = dill.load(f)

    def get_token(self):
        if not self.is_authenticated:
            self.con.refresh_token()
        token = self.con.token_backend.token
        return token['access_token']

    client.get_token = types.MethodType(get_token, client)
    return client
