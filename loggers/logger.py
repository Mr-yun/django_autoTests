# -*- coding:utf-8 -*-

import logging
import os
from logging import handlers


def remove_log_file(storage_path, file_prefix):
    file_list = os.listdir(storage_path)
    for file in file_list:
        if file.startswith(file_prefix):
            os.remove(storage_path + file)


def init_logger(log_level):
    logger = logging.getLogger('django_autoTests')
    log_file_name = 'django_autoTests.log'

    storage_path = './' + log_file_name

    fmt = '%(asctime)s|'
    fmt += '%(levelname)s|'
    fmt += '%(process)d|'
    fmt += '%(threadName)s|'
    fmt += '%(filename)s:%(lineno)s|'
    fmt += ' %(message)s'
    formatter = logging.Formatter(fmt)

    handler = handlers.RotatingFileHandler(
        storage_path, maxBytes=(16 * 1024 * 1024), backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)

    logger.setLevel(log_level)
    return logger


log = init_logger(logging.INFO)
