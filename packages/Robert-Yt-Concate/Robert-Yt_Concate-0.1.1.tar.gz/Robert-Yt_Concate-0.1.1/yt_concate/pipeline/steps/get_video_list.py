import json
import logging
import urllib

from yt_concate.pipeline.steps.step import Step
from yt_concate.setting import API_KEYS


class GetVideoList(Step):
    def process(self, data, inputs, utils):
        channel_id = inputs['channel_id']
        logger=logging.getLogger('yt_concate.logs')
        if utils.video_list_filepath_exist(channel_id):
            logger.warning('video file has already existed')
            return self.read_file(utils.get_video_list_filepath(channel_id))
        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

        first_url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(API_KEYS,
                                                                                                            channel_id)

        video_links = []
        url = first_url
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)

            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])

            try:
                next_page_token = resp['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
            except:
                break
        # print(video_links)
        self.write_to_file(video_links, utils.get_video_list_filepath(channel_id))
        return video_links

    def write_to_file(self, video_links, filepath):
        with open(filepath, 'w') as f:
            for video_link in video_links:
                f.write(video_link + '\n')

    def read_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return [url.strip() for url in f]
