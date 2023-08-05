import sys
import getopt
import logging

from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.downloads_captions_by_multithreading import DownloadCaptions
# from yt_concate.pipeline.steps.downloads_captions import DownloadCaptions
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.prefligjt import Preflight
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.read_captions import ReadCaption
from yt_concate.pipeline.steps.search import Search
# from yt_concate.pipeline.steps.downloads_videos import DownloadVideos
from yt_concate.pipeline.steps.downloads_videos_by_multithreading import DownloadVideos
from yt_concate.pipeline.steps.edit_videos import EditVideos
from yt_concate.utils import Utils
from yt_concate.logs import set_log

#CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'


def print_usage():
    print('python3 main.py OPTIONS')
    print('OPTIONS:')
    print('{:>6} {:<12} {}'.format("-c", "--channel_id", "channel id of the youtube channel"))
    print('{:>6} {:<12} {}'.format("-s", "--search_word", "word to be searched in the channel"))
    print('{:>6} {:<12} {}'.format("-l", "--limit", "limit of the amount of videos to be edited(default value:20)"))
    print('{:>6} {:<12} {}'.format(" ", "--cleanup", "remove all downloading caption and video \
    files after producing final output video"))
    print('{:>6} {:<12} {}'.format(" ", "--fast", "check if any downloading file already existed(default True)"))
    print('{:>6} {:<12} {}'.format(" ", "--logfile", "set the level of logging displayed on logfile"))
    print('{:>6} {:<12} {}'.format(" ", "--logstream", "set the level of logging displayed on terminal"))


def customize_log_level(type, arg, inputs):
    try:
        arg = int(arg)
        if arg in (10,20,30,40,50):
            inputs[type] = arg
        else:
            print('Not in range of logging ')
            print('set default logging.WARNING')
            inputs[type] = logging.DEBUG  # (10)
    except ValueError:
        logging.exception('You print an unavailable integer')
        sys.exit(2)


def main():
    inputs = {
        'channel_id': '',
        'search_word': '',
        'limit': 20,
        'cleanup': False,
        'fast': True,
        'logfile_level': logging.DEBUG,  # (10)
        'logstream_level': logging.DEBUG,  # (10)
    }

    short_opts = 'hc:s:l:'
    long_opts = 'help channel_id= search_word= limit= cleanup= fast= logfile= logstream='.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel_id'):
            inputs['channel_id'] = arg
        elif opt in ('-s', '--search_word'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            try:
                arg = int(arg)
                inputs['limit'] = arg
            except ValueError:
                logging.exception('You print an unavailable integer')
                sys.exit(2)
        elif opt == '--cleanup':
            inputs['cleanup'] = True
        elif opt == '--fast':
            inputs['fast'] = False
        elif opt == '--logfile':
            customize_log_level('logfile_level', arg, inputs)
        elif opt == '--logstream':
            customize_log_level('logstream_level', arg, inputs)

    while True:
        if not inputs['channel_id'] and not inputs['search_word']:
            print('You need to print a channel id and a search_word')
            print_usage()
            channel_id = input('Channel id:')
            search_word = input('Search Word:')
            inputs['channel_id'] = channel_id
            inputs['search_word'] = search_word
        else:
            break

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideos(),
        Postflight(),
    ]

    utils = Utils()
    set_log(inputs['logfile_level'], inputs['logstream_level'])
    if utils.output_filepath_exist(inputs['channel_id'], inputs['search_word']):
        logger = logging.getLogger('yt_concate.logs')
        logger.debug('This video has already existed')
        return
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
