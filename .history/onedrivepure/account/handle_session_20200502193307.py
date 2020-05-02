import dill


def save_session(client, path=''):
    """OneDriveClient, str->None
    
    Save the session info in a pickle file.
    
    Not safe, but whatever.
    """

    # client.auth_provider.save_session(path = path)
    c = dill.dumps(client)
    with open(path, 'wb') as f:
        f.write(c)
    return


def load_session(path=''):
    """str->OneDriveClient
    
    Determine whether the session is a normal or Business one,
    load a session from the storaged pickle,
    then refresh so the session is available to use immediately.
    """
    if not os.path.isfile(path):
        logging.error('Session dump path does not exist')
        raise Exception

    # # look inside the pickle to determine whether is normal or Business
    # session_standalone =onedrivesdk.auth_provider.Session.load_session(path = path)

    # if session_standalone.auth_server_url == 'https://login.microsoftonline.com/common/oauth2/token':
    #     # Business
    #         http = onedrivesdk.HttpProvider()
    #         auth = onedrivesdk.AuthProvider(http,
    #                                         client_id_business ,
    #                                         auth_server_url=auth_server_url,
    #                                         auth_token_url=auth_token_url)

    # client.auth_provider.load_session(path = path)

    # # refresh token so session good to use immediately
    # client.auth_provider.refresh_token()
    with open(path, 'rb') as f:
        client = dill.load(f)
    return client
