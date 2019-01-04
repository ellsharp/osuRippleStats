# coding: utf-8
# Referenced from 'pythonのlog出力 <https://qiita.com/yopya/items/63155923602bf97dec53>' by yopya.
# Thank you for yopya <3

import logging
import logging.handlers
import configparser

class logger:
    def __init__(self, name=__name__):
        name = name.replace('.py', '')
        # Defination of logger properties.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s][%(process)d][%(levelname)s][%(name)s]%(message)s")

        # include level debug
        log_level = 10
        # stdout
        handler = logging.StreamHandler()
        handler.setLevel(int(log_level))
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # fileout
        log_path = 'log/' + name + '.log'
        handler = logging.handlers.RotatingFileHandler(filename=log_path, maxBytes=11048576, backupCount=3)

        handler.setLevel(int(log_level))
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def __get_message_list():
        """
        Read message list file object and returns it.
        """
        message_list_path = 'conf/message.list'
        message_object = configparser.RawConfigParser()
        message_object.read(message_list_path, 'utf-8')
        return message_object

    def debug(self, message_code, *values):
        message_list = logger.__get_message_list()
        message = message_list['debug'][message_code]
        message = message % values
        self.logger.debug(message)

    def info(self, message_code, *values):
        message_list = logger.__get_message_list()
        message = message_list['info'][message_code]
        message = message % values
        self.logger.info(message)

    def warn(self, message_code, *values):
        message_list = logger.__get_message_list()
        message = message_list['warn'][message_code]
        message = message % values
        self.logger.warning(message)

    def error(self, message_code, *values):
        message_list = logger.__get_message_list()
        message = message_list['error'][message_code]
        message = message % values
        self.logger.error(message)

    def critical(self, message_code, *values):
        message_list = logger.__get_message_list()
        message = message_list['critical'][message_code]
        message = message % values
        self.logger.critical(message)
