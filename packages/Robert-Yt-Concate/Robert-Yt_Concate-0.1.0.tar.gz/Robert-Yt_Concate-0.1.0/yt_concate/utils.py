import os

from setting import DOWNLOADS_DIRS
from setting import CAPTIONS_DIRS
from setting import VIDEOS_DIRS
from setting import OUTPUT_DIRS


class Utils:

    def create_dirs(self):
        os.makedirs(DOWNLOADS_DIRS, exist_ok=True)
        os.makedirs(CAPTIONS_DIRS, exist_ok=True)
        os.makedirs(VIDEOS_DIRS, exist_ok=True)
        os.makedirs(OUTPUT_DIRS, exist_ok=True)

    def caption_file_exist(self, yt):
        path = yt.get_caption_filepath()
        return os.path.exists(path) and os.path.getsize(path) > 0

    def get_video_list_filepath(self, channel_id):
        return os.path.join(DOWNLOADS_DIRS, f'{channel_id}.txt')

    def video_list_filepath_exist(self, channel_id):
        return os.path.exists(self.get_video_list_filepath(channel_id)) \
               and os.path.getsize(self.get_video_list_filepath(channel_id)) > 0

    def get_output_filepath(self, channel_id, search_word):
        return os.path.join(OUTPUT_DIRS, channel_id + '__' + search_word + '.mp4')

    def output_filepath_exist(self,channel_id,search_word):
        return os.path.exists(self.get_output_filepath(channel_id,search_word)) \
               and os.path.getsize(self.get_output_filepath(channel_id,search_word))

