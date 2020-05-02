import argparse
import os


# Arguments
def parse_args():

    parser = argparse.ArgumentParser()

    # Set the config file location
    parser.add_argument('-chunk',
                        default=10(*1024**2),
                        type=int,)
    parser.add_argument('-workers',
                        default=10,
                        type=int,)
    parser.add_argument('-sharelink',
                        action='store_true',
                        default=False)
    
    parser.add_argument('-step',
                        default=102400,
                        type=int)
    # Set the config file location
    parser.add_argument('-conf',
                        default='./onedrive.json')


    # Script actions
    # Set mutually exclusive actions
    parser.add_argument('mode',
                        choices=['init_business', 'init', 'get', 'list', 'put', 'delete', 'mkdir', 'move', 'remote',
                                 'quota', 'share', 'direct', 'search'],

    # Return the parsed content
    args, rest=parser.parse_known_args()
    args.rest=rest
    return args
