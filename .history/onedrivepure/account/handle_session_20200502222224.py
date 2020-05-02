import dill


def save_session(client, path=''):
    c = dill.dumps(client)
    with open(path, 'wb') as f:
        f.write(c)
    return client


def load_session(path=''):
    with open(path, 'rb') as f:
        client = dill.load(f)
        def 
        @property
        def token(self):
            if self.is_authenticated:
                return 
            # token = self.con.token_backend.token
            if self.is_authenticated:
                raise RuntimeError('Token not found.')
            elif token.is_access_expired:
                self.con.refresh_token()
                token = self.con.token_backend.token
            return token['access_token']

        return client
