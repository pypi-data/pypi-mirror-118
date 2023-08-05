from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
import logging

from yt_concate.pipeline.steps.step import Step


class EditVideos(Step):

    def process(self, data, inputs, utils):
        clips = []
        logger=logging.getlogger('yt_concate.logs')
        for found in data:
            videopath = found.yt.video_filepath
            start, end = found.time.split('-->')
            video = VideoFileClip(videopath).subclip(float(start), float(end))
            clips.append(video)
            if len(clips) > inputs['limit']:
                break
        final_clip = concatenate_videoclips(clips)
        channel_id, search_word = inputs['channel_id'], inputs['search_word']
        final_clip.write_videofile(utils.get_output_filepath(channel_id, search_word))
