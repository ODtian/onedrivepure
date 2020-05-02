import os
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import JoinableQueue
from queue import Queue, Empty

from ..share_link import handle_link
from ..utils.bar_custom import count_bar, message_bar, sleep_bar
from ..utils.help_func import norm_path
from .file_uploader import get_upload_url, upload_file, upload_remote


def get_path(local_paths, remote_base_path):
    file_list = []
    for path in local_paths:
        if os.path.isfile(path):
            name = os.path.basename(path)
            remote_path = norm_path(
                os.path.join(remote_base_path, name)
            )
            file_list.append((path, remote_path))
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


def put(client, args):
    local_paths = args.rest[:-1]
    remote_base_path = args.rest[-1]

    if not args.sharelink:
        file_list = get_path(local_paths, remote_base_path)

        q = JoinableQueue()
        sleep_q = Queue()

        [q.put(i) for i in file_list]

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
                    remote_path='OD:'+remote_path,
                    message='文件已存在'
                )

            elif status == 'bad':
                q.put(task)
                message_bar(
                    remote_path='OD:'+remote_path,
                    message='错误 稍后重试'
                )
            q.task_done()
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            while True:
                if q._unfinished_tasks._semlock._is_zero():
                    break
                if not sleep_q.empty():
                    sleep_time = sleep_q.get()
                    sleep_bar(sleep_time=sleep_time)
                    sleep_q.queue.clear()
                else:
                    try:
                        task = q.get(timeout=0.5)
                    except Empty:
                        continue
                    else:
                        executor.submit(do_task, task)
                        time.sleep(0.05)

    else:
        data, share_link = handle_link(
            args.sharelink, args.save_dir, show_json=False
        )
        q = JoinableQueue()
        sleep_q = Queue()

        [q.put(t) for t in data]

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
                    remote_path='OD:'+remote_path,
                    message='文件已存在'
                )
            elif status == 'bad':
                q.put(task)
                message_bar(
                    remote_path='OD:'+remote_path,
                    message='错误 稍后重试'
                )
            q.task_done()
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            while True:
                if q._unfinished_tasks._semlock._is_zero():
                    break
                if not sleep_q.empty():
                    sleep_time = sleep_q.get()
                    sleep_bar(sleep_time=sleep_time)
                    sleep_q.queue.clear()
                else:
                    try:
                        task = q.get(timeout=0.5)
                    except Empty:
                        continue
                    else:
                        executor.submit(do_task, task)
                        time.sleep(0.05)
        return client
