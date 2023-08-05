from __future__ import unicode_literals
import logging

import youtube_dl

from yt_concate.pipeline.steps.step import Step


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('yt_concate.logs')
        yt_set = {found.yt for found in data}
        for yt in yt_set:
            if yt.video_filepath_exist():
                logger.warning(f'Video:{yt.url} has already existed')
                continue
            ydl_opts = {
                'format': 'worst',  # 畫質
                'outtmpl': yt.get_video_filepath(),  # 輸出模板：裝著路徑以及檔名
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                logger.debug('downloading', yt.url)
                ydl.download([yt.url])

        return data
