import json
import os
import time

import requests
from tqdm import tqdm

from fileUploader import get_upload_url, upload_file, upload_remote

from ..sharelink import handle_link
from ..utils.shop import Shop
from ..utils.utils import get_now_time, norm_path


def get_path(local_paths, remote_base_path):
    file_list = []
    for path in local_paths:
        if os.path.isfile(path):
            name = os.path.basename(path)
            remote_path = norm_path(
                os.path.join(remote_base_path, name)
            )
            # file_list.append((path, remote_path))

        else:
            bar_format = '{desc} {n} folders done [{postfix[0]}]'
            bar = tqdm(
                bar_format=bar_format,
                desc=get_now_time(),
                postfix=['']
            )
            for root, _, files in os.walk(path):
                for name in files:
                    local_path = os.path.join(root, name)
                    remote_path = norm_path(
                        os.path.join(root[len(path):], name)
                    )
                    file_list.append((local_path, remote_path))
                bar.postfix = [root]
                bar.update(1)
            bar.close()
    return file_list


def exist_bar(remote_path):
    bar_format = '{desc} [存在同名文件 OD:{postfix[0]}]'
    bar = tqdm(
        desc=get_now_time(),
        postfix=[remote_path],
        bar_format=bar_format
    )
    bar.close()


def sleep_bar(sleep_time):
    message = 'API频率限制，睡眠{}秒'
    bar_format = '{desc} [{postfix[0]}]'
    bar = tqdm(
        desc=get_now_time(),
        postfix=[message.format(sleep_time)],
        bar_format=bar_format
    )

    for _ in range(sleep_time):
        time.sleep(1)
        sleep_time -= 1
        bar.postfix = \
            [message.format(sleep_time)]
        bar.close()


def do_put(client, args):
    local_paths = args.rest[:-1]
    remote_base_path = args.rest[-1]

    def producer(task, raw_queue):
        remote_path = task[1]
        status, upload_url, sleep_time = \
            get_upload_url(client, remote_path)
        if status == 'good':
            return (
                task[0],
                upload_url
            )

        elif status == 'exist':
            exi
        elif status == 'sleep':
            raw_queue.put(task)
            sleep_bar(sleep_time)

        elif status == 'failed':
            raw_queue.put(task)
            bar_format = '{desc} [错误-稍后重试 OD:{postfix[0]}]'
            bar = tqdm(
                desc=get_now_time(),
                postfix=[remote_path],
                bar_format=bar_format
            )
            bar.close()

    if not args.sharelink:
        file_list = get_path(local_paths, remote_base_path)

        def consumer(executor, task):
            future = executor.submit(
                upload_file, task, args.chunk, args.step
            )
            return future

        def callback(res, raw_queue):
            result = res.result()
            if result is not True:
                raw_queue.put(result)

        shop = Shop(max_shell=args.batchnum)
        shop.set_tasks(file_list)
        shop.set_producer(producer)
        shop.set_consumer(consumer, callback)
        shop.run(max_workers=args.workers, sleep_time=0.1)
    else:
        # file_list = files, share_link = handle_link(share_link)
        data, sharelink = handle_link(args.sharelink)
        for task in data:
            task['path'] = norm_pathtask['path']

        def consumer(executor, task):
            future = executor.submit(
                upload_remote, task, args.chunk, args.step
            )
            return future
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            for share_link in from_list:
                files, share_link = handle_link(share_link)
                fail_task = {'link': share_link, 'data': []}
                for file in files:
                    download_url = file['download_url']
                    size = file['size']
                    path = file['path']
                    total_path = '/' + \
                        '/'.join(list(filter(None,
                                             target_dir.split('/')[1:]
                                             + path.split('/'))))
                    headers = {
                        'Authorization': 'bearer {}'.format(client.token),
                        'Content-Type': 'application/json'
                    }
                    info = json.dumps(
                        {
                            'item': {
                                '@microsoft.graph.conflictBehavior': 'fail',
                                'name': os.path.basename(total_path)}
                        }
                    )
                    api_url = 'https://graph.microsoft.com/v1.0'\
                        '/me/drive/root:{}:/createUploadSession'\
                        .format(total_path)
                    for i in range(6):
                        req = requests.post(
                            api_url, headers=headers, data=info)
                        code = req.status_code
                        if code < 400:  # 成功
                            executor.submit(upload_remote,
                                            download_url,
                                            size, total_path,
                                            req.json()['uploadUrl'],
                                            share_link)
                            break
                        elif code == 409:  # 这个说明文件已经存在了
                            bar_format = '{desc} [Exist od:{postfix[0]}]'
                            with tqdm(desc=_time(), postfix=[
                                    total_path], bar_format=bar_format):
                                break
                        elif code == 429 and i <= 5:  # 409频次限制，暂停两分钟
                            print(req.headers)
                            later = int(req.headers.get('Retry-After'))
                            bar_format = '{desc} [Sleep {postfix[0]}]'
                            with tqdm(desc=_time(),
                                      postfix=['API频次限制，睡眠{}秒'.format(later)],
                                      bar_format=bar_format):
                                time.sleep(later)

                        elif i == 5:  # 重试次数耗尽，下次再来吧
                            bar_format = '{desc} [Error {postfix[0]}]'
                            with tqdm(desc=_time(),
                                      postfix=['创建文件失败，呆会再试！{}'.format(code)],
                                      bar_format=bar_format):
                                fail_task['data'].append(file)
                                break
                        else:
                            time.sleep(0.3)  # 发生未知错误，再试一次
                if len(fail_task['data']) > 0:
                    json.dump(fail_task, open(
                        'fail_'+str(time.time())+'.txt', 'w'))
    return client
