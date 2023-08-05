from yt_concate.pipeline.steps.step import Step


class ReadCaption(Step):
    def process(self, data, inputs, utils):
        for yt in data:
            if not utils.caption_file_exist(yt):
                continue
            captions = {}
            with open(yt.get_caption_filepath(), 'r') as f:
                for line in f:
                    if '-->' in line:
                        time = line.strip()
                        time_line = True
                        continue
                    if time_line:
                        caption = line.strip()
                        captions[caption] = time
                        time_line = False
            yt.captions = captions

        return data
