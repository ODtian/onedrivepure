from tqdm import tqdm
from helpFunc import get_now_time


def message_bar(remote_path, message=''):
    bar_format = '{desc} ['+message+' OD:{postfix[0]}]'
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


def count_bar(message,):
    bar_format = '{desc} {n} '+message+' [{postfix[0]}]'
    bar = tqdm(
        bar_format=bar_format,
        desc=get_now_time(),
        postfix=['']
    )
    return bar
