import logging


def get_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel('INFO')
    return logger
