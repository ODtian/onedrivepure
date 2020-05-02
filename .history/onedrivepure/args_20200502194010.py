import argparse
import os


# Arguments
def parse_args():

    parser = argparse.ArgumentParser()

    # Set the config file location
    parser.add_argument('-chunk',
                        default=10(*1024**2),
                        type=int,
                        help='Set the chunk size when uploading, use with -hack, must be times of 327680. Max is 62914560.')
    parser.add_argument('-workers',
                        default=10,
                        type=int,
                        help='Set the number of workers in multi-thread uploading')
    # parser.add_argument('-batchnum',
    #                     default=10,
    #                     type=int,
    #                     help='Set the number of batchnum in multi-thread uploading')
    parser.add_argument('-sharelink',
                        action='store_true',
                        default=False,
                        help='Switch the mode of upload, if is Ture the client will upload the file in sharelink'
                        '(arg\'s position used to be the local file) automatically')
    parser.add_argument('-step',
                        default=102400,
                        type=int,
                        help='Set the step size of progress bar')
    # Set the config file location
    parser.add_argument('-conf',
                        default='./onedrive.json',
                        help='Set the location of config file')


    # Set the logging level
    parser.add_argument('-verbose',
                        action='store',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='WARNING',
                        help='Set the logging level')

    # Show full path instead of short one while listing
    parser.add_argument('-fullpath',
                        action='store_true',
                        default=False,
                        help='Show full path instead of short one while listing')

    # Script actions
    # Set mutually exclusive actions
    parser.add_argument('mode',
                        choices=['init_business', 'init', 'get', 'list', 'put', 'delete', 'mkdir', 'move', 'remote',
                                 'quota', 'share', 'direct', 'search'],

    # Return the parsed content
    args, rest=parser.parse_known_args()
    args.rest=rest
    return args
