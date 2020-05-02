import dill


def save_session(client, path=''):
    c = dill.dumps(client)
    with open(path, 'wb') as f:
        f.write(c)
    return


def load_session(path=''):
    if not os.path.isfile(path):
        logging.error('Session dump path does not exist')
        raise Exception

    with open(path, 'rb') as f:
        client = dill.load(f)
    return client
