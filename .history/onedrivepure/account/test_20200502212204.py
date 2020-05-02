from O365 import Account
my_client = (
    '6fdb55b4-c905-4612-bd23-306c3918217c',
    'HThkLCvKhqoxTDV9Y9uS+EvdQ72fbWr/Qrn2PFBZ/Ow='
)
account = Account(my_client)
account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint_dl'], redirect_uri=)
print(account.get_current_user())
