import argparse
import json
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("-chunk", default=30 * (1024 ** 2), type=int)

    parser.add_argument("-workers", default=5, type=int)

    parser.add_argument("-sharelink", action="store_true", default=False)

    parser.add_argument("-step", default=1024 ** 2, type=int)

    parser.add_argument("-app", default=0, type=int)

    parser.add_argument(
        "-conf", default=os.path.join(BASE_DIR, "..", "onedrive.json"), type=str
    )

    parser.add_argument("-client-id", default="", type=str)

    parser.add_argument("-client-secret", default="", type=str)

    parser.add_argument("-redirect-uri", default="", type=str)

    parser.add_argument("-show-json", action="store_true", default=True)

    parser.add_argument(
        "-save-dir", default=os.path.join(BASE_DIR, "..", "account_storage"), type=str
    )

    parser.add_argument("-save-account-name", default="", type=str)

    parser.add_argument("-sleep-time", default=0.1, type=int)

    # actions = [
    #     'init_business', 'init', 'get', 'list',
    #     'put', 'delete', 'mkdir', 'move', 'remote',
    #     'quota', 'share', 'direct', 'search'
    # ]

    actions = ["init", "upload", "link"]
    parser.add_argument("mode", choices=actions)

    args, rest = parser.parse_known_args()

    if os.path.exists(args.conf):
        conf = json.load(open(args.conf, "r"))
        args.conf = conf
        for key, value in conf.items():
            if not hasattr(args, key):
                setattr(args, key, value)
    args.rest = rest
    return args
