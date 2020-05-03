import os
import time

from .data_iter import dataIter


def get_now_time():
    return '['+time.strftime('%H:%M:%S', time.localtime())+']'


def get_headers(client, content_type='application/json'):
    headers = {
        'Authorization': 'Bearer {}'.format(client.get_token()),
        'Content-Type': content_type
    }
    return headers


def get_data(file_piece, bar, step_size=1024*10):
    return dataIter(file_piece, bar, step_size)


def norm_path(path):
    norm = os.path.normpath(path)\
        .replace('\\', '/').strip('/')
    return norm


def get_remote_base_path(path):
    return '/'.join(path.split('/')[1:])
