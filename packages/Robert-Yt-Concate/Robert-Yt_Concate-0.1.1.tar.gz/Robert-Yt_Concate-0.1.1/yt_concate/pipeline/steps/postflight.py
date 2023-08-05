import logging
import shutil

from yt_concate.pipeline.steps.step import Step
from yt_concate.setting import CAPTIONS_DIRS
from yt_concate.setting import VIDEOS_DIRS


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('yt_concate.logs')
        if inputs['cleanup']:
            if utils.output_filepath_exist(inputs['channel_id'], inputs['search_word']):
                try:
                    shutil.rmtree(CAPTIONS_DIRS)
                    shutil.rmtree(VIDEOS_DIRS)
                except OSError as e:
                    print(f"Error:{e.strerror}")
        logger.debug('in Postflight')
