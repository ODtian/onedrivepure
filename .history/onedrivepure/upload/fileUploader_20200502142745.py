import os
import time

import requests

from ..utils.utils import (
    get_data, get_headers, get_now_time, 
    # get_single_request,
    norm_path
)

# from ..tqdm.autonotebook import tqdm
from tqdm import tqdm

# def get_upload_url(client, tasks):
#     API_HOST = 'https://graph.microsoft.com/v1.0'
#     headers = get_headers(client)
#     data = json.dumps({
#         'requests': [
#             get_single_request(task['total_path'], index)
#             for index, task in enumerate(tasks)
#         ]
#     })
#     res = requests.post(API_HOST+'/$batch', headers=headers, data=data)

#     if res.status_code == 200:
#         successed = []
#         failed = []
#         for i in res.json()['responses']:
#             code = i['status']
#             this_id = int(i['id'])-1
#             this_task = tasks[this_id]

#             if code == 200:
#                 this_task['upload_url'] = i['body']['uploadUrl']
#                 this_task['status'] = 'success'
#                 successed.append(this_task)

#             elif code == 409:
#                 this_task['status'] = 'finish'
#                 successed.append(this_task)

#             elif code == 429:
#                 sleep_time = int(i['headers'].get('Retry-After'))
#                 return [], tasks, sleep_time

#             else:
#                 failed.append(this_task)

#         return successed, failed, 0
#     else:
#         return [], tasks, 0


def get_upload_url(client, remote_path):
    API_HOST = 'https://graph.microsoft.com/v1.0'

    url = API_HOST + \
        '/me/drive/root:{}:/createUploadSession'.format(remote_path)

    headers = get_headers(client)

    data = {
        'item': {
            '@microsoft.graph.conflictBehavior': 'fail',
            'name': os.path.basename(remote_path)
        }
    }

    r = requests.post(url, headers=headers, data=data)
    result = r.json()
    code = r.status_code
    if code == 200:
        return 'good', result['uploadUrl'], 0
    elif code == 409:
        return 'exist', '', 0
    elif code == 429:
        sleep_time = r.headers.get('Retry-After')
        return 'sleep', '', int(sleep_time)
    else:
        return 'bad', '', 0


def upload_piece(upload_url, local_path, file_range, file_size, step_size, bar
                 ):
    start, end = file_range
    content_length = end - start + 1
    headers = {
        'Content-Range': 'bytes {}-{}/{}'.format(start, end, file_size),
        'Content-Length': str(content_length)
    }

    with open(local_path, 'rb') as f:
        f.seek(file_range[0])
        file_piece = f.read(content_length)

        data = get_data(file_piece, bar)
        req = requests.put(upload_url, headers=headers, data=data)

        return req.status_code


def upload_file(task, chunksize, step_size):
    try:
        local_path, upload_url = task
        file_size = os.path.getsize(local_path)
        range_list = [
            [i, i + chunksize - 1]
            for i in range(0, file_size, chunksize)
        ]
        range_list[-1][-1] = file_size - 1

        bar_format = \
            '{desc} {percentage: >6.2f}% |{bar:20}| [{n}/{total}] '\
            '{rate} [{elapsed}/{remaining}] [Upload {postfix[0]}]'

        bar = tqdm(
            total=file_size,
            desc=get_now_time(),
            postfix=[local_path],
            bar_format=bar_format,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        )

        for file_range in range_list:
            code = upload_piece(
                upload_url=upload_url,
                local_path=local_path,
                file_range=file_range,
                file_size=file_size,
                step_size=step_size,
                bar=bar
            )
            if not (code == 202 or code == 201):
                return task
        bar.close()
        return True
    except Exception:
        return task


def try_get_remote_file(session, download_url, max_retry=5, sleep_time=1):
    for n in range(max_retry):
        remote_file = session.get(download_url, stream=True)
        code = remote_file.status_code
        if code == 200:
            return remote_file
        elif n == max_retry-1:
            bar_format = '{desc} [Error {postfix[0]}]'
            bar = tqdm(
                desc=get_now_time(),
                postfix=['获取远程文件失败 {}'.format(code)],
                bar_format=bar_format
            )
            bar.close()
            return
        else:
            time.sleep(sleep_time)


def upload_remote(share_link, download_url, file_size, total_path, upload_url):
    try:
        download_url = task
        session = requests.session()
        session.get(share_link)
        bar_format = \
            '{desc} {percentage: >6.2f}% |{bar:20}| [{n}/{total}] '\
            '{rate} [{elapsed}/{remaining}] [Upload {postfix[0]}]'

        bar = tqdm(
            total=file_size,
            desc=get_now_time(),
            postfix=[total_path],
            bar_format=bar_format,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        )

        remote_file = try_get_remote_file(session, download_url)
        if not remote_file:
            return

        start = 0

        for chunk in remote_file.iter_content(30*1024*1024):
            content_length = len(chunk)
            end = start + content_length - 1

            headers = {
                'Content-Range': 'bytes {}-{}/{}'
                .format(start, end, file_size),
                'Content-Length': str(content_length)
            }

            data = get_data(chunk, bar)

            req = requests.put(upload_url, headers=headers, data=data)
            code = req.status_code

            if not (code == 202 or code == 201):
                return task

            start = end + 1

        bar.close()
        return True

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    pass
