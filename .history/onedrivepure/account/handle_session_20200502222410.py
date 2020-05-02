import dill


def save_session(client, path=''):
    c = dill.dumps(client)
    with open(path, 'wb') as f:
        f.write(c)
    return client


def load_session(path=''):
    with open(path, 'rb') as f:
        client = dill.load(f)

        @property
        def token(self):
            if not self.is_authenticated:
                return
            # token = self.con.token_backend.token
            return token['access_token']

        return client
