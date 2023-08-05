import logging
from concurrent import futures
import time

from youtube_transcript_api import YouTubeTranscriptApi

from yt_concate.pipeline.steps.step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        with futures.ThreadPoolExecutor(max_workers=30) as executor:
            [executor.submit(self.write_captions, yt, inputs, utils) for yt in data]
        end = time.time()
        print(end - start)
        return data

    def write_captions(self, yt, inputs, utils):
        logger = logging.getLogger('yt_concate.logs')
        if inputs['fast']:
            if utils.caption_file_exist(yt):
                logger.warning('Caption File Has already downloaded')
                return
            else:
                srt = self.generate_captions(yt, logger)
        else:
            srt = self.generate_captions(yt, logger)
        if not srt:
            return
        # save the caption to a file named Output.txt
        with open(yt.caption_filepath, "w", encoding='utf-8') as text_file:
            for caption in srt:
                text_file.write(f"{caption['start']}-->{caption['start'] + caption['duration']:.2f}\n")
                text_file.write(f"{caption['text']}\n")

    def generate_captions(self, yt, logger):
        try:
            srt = YouTubeTranscriptApi.get_transcript(yt.id, languages=['en'])
            logger.info('success')
        except:
            print('Error when downloading caption for', yt.url)
        else:
            return srt
