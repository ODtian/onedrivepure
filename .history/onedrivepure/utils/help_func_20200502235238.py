import os
import time
from .data_iter import dataIter


# def get_single_request(path, index):
#     single_request = {
#         'id': str(index+1),
#         'method': 'POST',
#         'url': '/me/drive/root:{}:/createUploadSession'.format(path),
#         'headers': {
#             'Content-Type': 'application/json'
#         },
#         'body': {
#             'item': {
#                 '@microsoft.graph.conflictBehavior': 'fail',
#                 'name': os.path.basename(path)
#             }
#         }}
#     return single_request


def get_now_time():
    return '['+time.strftime('%H:%M:%S', time.localtime())+']'


def get_headers(client, content_type='application/json'):
    headers = {
        'Authorization': 'bearer {}'.format(client.get_token()),
        'Content-Type': content_type
    }
    return headers


def get_data(file_piece, bar, step_size=1024*10):
    return dataIter(file_piece, bar, step_size)


def norm_path(path):
    norm = os.path.normpath(path).replace('\\', '/').strip('/')
    strips = norm.lstrip('od').lstrip(':')
    return strips
