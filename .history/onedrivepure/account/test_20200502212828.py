from O365 import Account
from static import default_client, default_redirect_url
account = Account(my_client)
account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint_dl'], redirect_uri=)
print(account.get_current_user())
