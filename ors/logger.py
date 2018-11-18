# coding: utf-8
# Referenced from 'pythonのlog出力 <https://qiita.com/yopya/items/63155923602bf97dec53>' by yopya.
# Thank you for yopya <3

import logging
import logging.handlers

class logger:
    def __init__(self, name=__name__):
        # Defination of logger properties.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s][%(process)d][%(name)s][%(levelname)s]%(message)s")

        # include level debug
        log_level = 10
        # stdout
        handler = logging.StreamHandler()
        handler.setLevel(int(log_level))
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # fileout
        log_path = 'log/ors.log'
        handler = logging.handlers.RotatingFileHandler(filename=log_path, maxBytes=11048576, backupCount=3)

        handler.setLevel(int(log_level))
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
