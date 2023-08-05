from __future__ import unicode_literals
import logging
from concurrent import futures
import time

import youtube_dl

from yt_concate.pipeline.steps.step import Step


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        logger = logging.getLogger('yt_concate.logs')
        yt_set = {found.yt for found in data}
        with futures.ThreadPoolExecutor(max_workers=40) as executor:
            [executor.submit(self.download_video, yt, inputs, logger) for yt in yt_set]
        end = time.time()
        print(end - start)
        return data

    def download_video(self, yt, inputs, logger):
        if inputs['fast']:
            if yt.video_filepath_exist():
                logger.warning(f'Video:{yt.url} has already existed')
                return
        ydl_opts = {
            'format': 'worst',  # 畫質
            'outtmpl': yt.get_video_filepath(),  # 輸出模板：裝著路徑以及檔名
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                logger.info(f'downloading{yt.url}')
                ydl.download([yt.url])
        except:
            logger.error('Video downloading error')
