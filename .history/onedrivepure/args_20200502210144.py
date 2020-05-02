import argparse
import json
import os
# Arguments


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-chunk',
                        default=10*(1024**2),
                        type=int,)
    parser.add_argument('-workers',
                        default=10,
                        type=int)
    parser.add_argument('-sharelink',
                        action='store_true',
                        default=False)

    parser.add_argument('-step',
                        default=102400,
                        type=int)

    parser.add_argument('-app',
                        default=0,
                        type=int)
    parser.add_argument('-conf',
                        default='./onedrive.json')
    parser.add_argument('-client-id', default=)

    actions = [
        'init_business', 'init', 'get', 'list',
        'put', 'delete', 'mkdir', 'move', 'remote',
        'quota', 'share', 'direct', 'search'
    ]
    parser.add_argument('mode', choices=actions)

    # Return the parsed content
    args, rest = parser.parse_known_args()

    if os.path.exists(args.conf):
        conf = json.load(open(args.conf, 'r'))
        args.conf = conf
        for key, value in conf.items():
            if not args.hasattr(key):
                args.setattr(key, value)
    args.rest = rest
    return args
