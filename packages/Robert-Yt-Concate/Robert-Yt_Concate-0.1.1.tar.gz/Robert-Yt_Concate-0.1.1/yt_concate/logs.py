import logging

def set_log(file_level,stream_level):
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter=logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

    file_handler=logging.FileHandler('youtube.log')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    stream_handler=logging.StreamHandler()
    stream_handler.setLevel(stream_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

