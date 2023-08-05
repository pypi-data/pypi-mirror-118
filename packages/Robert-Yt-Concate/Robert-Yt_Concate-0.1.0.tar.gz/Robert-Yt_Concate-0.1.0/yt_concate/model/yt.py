import os

from yt_concate.setting import CAPTIONS_DIRS
from yt_concate.setting import VIDEOS_DIRS


class YT:
    def __init__(self, url):
        self.url = url
        self.id = YT.get_video_id_from_url(self.url)
        self.caption_filepath = self.get_caption_filepath()
        self.video_filepath = self.get_video_filepath()
        self.captions = None

    @staticmethod
    def get_video_id_from_url(url):
        return url.split('watch?v=')[-1]

    def get_caption_filepath(self):
        return os.path.join(CAPTIONS_DIRS, self.id + '.txt')

    def get_video_filepath(self):
        return os.path.join(VIDEOS_DIRS, self.id + '.mp4')

    def video_filepath_exist(self):
        return os.path.exists(self.video_filepath) \
               and os.path.getsize(self.video_filepath) > 0

    def __str__(self):
        return f'(<YT({self.id}>)'

    def __repr__(self):
        content = ' ; '.join([
            'yt=' + str(self.id),
            'caption=' + str(self.caption_filepath),
            'video=' + str(self.video_filepath)
        ])
        return '<Found(' + content + ')>'
