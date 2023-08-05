import logging

from yt_concate.pipeline.steps.step import Step


class Preflight(Step):
    def process(self, data, inputs, utils):
        logger=logging.getLogger('yt_concate.logs')
        logger.debug('in Preflight')
        utils.create_dirs()
