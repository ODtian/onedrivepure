import os
import time

import requests

from ..utils.bar_custom import message_bar, upload_bar
from ..utils.help_func import get_data, get_headers


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
    print(result)
    if code == 200:
        return 'good', result['uploadUrl'], 0
    elif code == 409:
        return 'exist', '', 0
    elif code == 429:
        sleep_time = r.headers.get('Retry-After')
        return 'sleep', '', int(sleep_time)
    else:
        return 'bad', '', 0


def upload_piece(
    upload_url,
    local_path,
    file_range,
    file_size,
    step_size,
    bar
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

        data = get_data(file_piece, bar, step_size=step_size)
        req = requests.put(upload_url, headers=headers, data=data)

        return req.status_code


def upload_file(local_path, upload_url, chunk_size, step_size):
    try:
        file_size = os.path.getsize(local_path)
        range_list = [
            [i, i + chunk_size - 1]
            for i in range(0, file_size, chunk_size)
        ]
        range_list[-1][-1] = file_size - 1

        bar = upload_bar(file_size, local_path)
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
                bar.close()
                return False
        bar.close()
        return True
    except Exception:
        return False


def try_get_remote_file(session, download_url, max_retry=5, sleep_time=1):
    for n in range(max_retry):
        remote_file = session.get(download_url, stream=True)
        code = remote_file.status_code
        if code == 200:
            return remote_file
        elif n == max_retry-1:
            message_bar(remote_path='获取远程文件失败 {} {}'.format(
                code, code))
            return False
        else:
            time.sleep(sleep_time)


def upload_remote(
    download_url,
    upload_url,
    share_link,
    file_size,
    remote_path,
    chunk_size,
    step_size
):
    try:
        session = requests.session()
        session.get(share_link)

        remote_file = try_get_remote_file(session, download_url)
        if not remote_file:
            return False

        bar = upload_bar(file_size, remote_path)
        start = 0

        for chunk in remote_file.iter_content(chunk_size):
            content_length = len(chunk)
            end = start + content_length - 1

            headers = {
                'Content-Range': 'bytes {}-{}/{}'
                .format(start, end, file_size),
                'Content-Length': str(content_length)
            }

            data = get_data(chunk, bar, step_size=step_size)

            req = requests.put(upload_url, headers=headers, data=data)
            code = req.status_code

            if not (code == 202 or code == 201):
                bar.close()
                return False

            start = end + 1

        bar.close()
        return True

    except Exception:
        return False


if __name__ == '__main__':
    pass
