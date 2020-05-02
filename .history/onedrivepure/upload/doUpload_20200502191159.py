import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import requests
from tqdm import tqdm

from fileUploader import get_upload_url, upload_file, upload_remote

from ..sharelink import handle_link
from ..utils.barCustom import count_bar, message_bar, sleep_bar
from ..utils.helpFunc import get_now_time, norm_path
# from ..utils.shop import Shop


def get_path(local_paths, remote_base_path):
    file_list = []
    for path in local_paths:
        if os.path.isfile(path):
            name = os.path.basename(path)
            remote_path = norm_path(
                os.path.join(remote_base_path, name)
            )
        else:
            bar = count_bar(message='个文件夹已完成')
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


def do_put(client, args):
    local_paths = args.rest[:-1]
    remote_base_path = args.rest[-1]

    if not args.sharelink:
        file_list = get_path(local_paths, remote_base_path)
        q = Queue()

        for i in file_list:
            q.put(i)

        sleep_q = Queue()

        def do_task(task):
            local_path, remote_path = task
            status, upload_url, sleep_time = \
                get_upload_url(client, remote_path)
            if status == 'good':
                result = upload_file(
                    local_path=local_path,
                    upload_url=upload_url,
                    chunk_size=args.chunk,
                    step_size=args.step
                )
                if result is not True:
                    q.put(task)
            
            elif status == 'sleep':
                q.put(task)
                sleep_q.put(sleep_time)
            
            elif status == 'exist':
                message_bar(
                    remote_path=remote_path,
                    message='文件已存在'
                )
            
            elif status == 'failed':
                q.put(task)
                message_bar(
                    remote_path=remote_path,
                    message='错误 稍后重试'
                )

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            while True:
                if not sleep_q.empty():
                    sleep_time = sleep_q.get()
                    sleep_bar(sleep_time=sleep_time)
                    sleep_q.queue.clear()
                else:
                    task = q.get()
                    executor.submit(do_task, task)
                    time.sleep(0.05)

        # def producer(task, raw_queue):
        #     remote_path = task[1]
        #     status, upload_url, sleep_time = \
        #         get_upload_url(client, remote_path)

        #     if status == 'good':
        #         return (task[0], upload_url)
        #     elif status == 'sleep':
        #         raw_queue.put(task)
        #         sleep_bar(sleep_time=sleep_time)
        #     elif status == 'exist':
        #         message_bar(
        #             remote_path=remote_path,
        #             message='文件已存在'
        #         )
        #     elif status == 'failed':
        #         raw_queue.put(task)
        #         message_bar(
        #             remote_path=remote_path,
        #             message='错误 稍后重试'
        #         )

        # def consumer(executor, task):
        #     future = executor.submit(
        #         upload_file, task, args.chunk, args.step
        #     )
        #     return future

        # def callback(res, raw_queue):
        #     result = res.result()
        #     if result is not True:
        #         raw_queue.put(result)

        # shop = Shop(max_shell=args.batchnum)
        # shop.set_tasks(file_list)
        # shop.set_producer(producer)
        # shop.set_consumer(consumer, callback)
        # shop.run(max_workers=args.workers, sleep_time=0.1)
    else:
        # file_list = files, share_link = handle_link(share_link)
        data, share_link = handle_link(args.sharelink)
        file_list = get_path(local_paths, remote_base_path)
        q = Queue()

        for t in data:
            q.put(t)

        sleep_q = Queue()

        def do_task(task):
            download_url = task.get('download_url')
            file_size = task.get('size')
            remote_path = norm_path(os.path.join(
                remote_base_path,
                task.get('path')
            ))

            status, upload_url, sleep_time = \
                get_upload_url(client, remote_path)

            if status == 'good':
                result = upload_remote(
                    download_url=download_url,
                    upload_url=upload_url,
                    share_link=share_link,
                    file_size=file_size,
                    remote_path=remote_path,
                    chunk_size=args.chunk,
                    step_size=args.step
                )
                if result is not True:
                    q.put(task)
            elif status == 'sleep':
                q.put(task)
                sleep_q.put(sleep_time)
            elif status == 'exist':
                message_bar(
                    remote_path=remote_path,
                    message='文件已存在'
                )
            elif status == 'failed':
                q.put(task)
                message_bar(
                    remote_path=remote_path,
                    message='错误 稍后重试'
                )

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            while True:
                if not sleep_q.empty():
                    sleep_time = sleep_q.get()
                    sleep_bar(sleep_time=sleep_time)
                    sleep_q.queue.clear()
                else:
                    task = q.get()
                    executor.submit(do_task, task)
                    time.sleep(0.05)
        return client
