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
        return client
