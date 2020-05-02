import dill
import os

def get_save_path(args):
    save_path = os.path.join(save_dir, 
    args.save_account_name)
def save_session(client, path=''):
    client_saved = dill.dumps(client)
    with open(path, 'wb') as f:
        f.write(client_saved)
    return client


def load_session(path=''):
    with open(path, 'rb') as f:
        client = dill.load(f)

    @property
    def token(self):
        if not self.is_authenticated:
            self.con.refresh_token()
        token = self.con.token_backend.token
        return token['access_token']
    
    client.token = token

    return client
