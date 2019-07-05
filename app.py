import os
import util
from kws_test import kws_detect

CONFIG_1 = 'VC_Config1.txt'
CONFIG_2 = 'VC_Config2.txt'


class Config(object):
    def __init__(self):
        self.config_file_1 = CONFIG_1
        self.config_file_2 = CONFIG_2
        self.cfg_dict_1 = {}
        self.cfg_dict_2 = {}

        self.parse_config()

    def parse_config(self):
        self.cfg_dict_1 = util.read_config(self.config_file_1)
        self.cfg_dict_2 = util.read_config(self.config_file_2)


class VC_app(object):
    def __init__(self):
        self.cfg_obj = Config()
        self.kws_obj = kws_detect()
        
    def start(self):
        self.kws_obj.run()


if __name__ == '__main__':
    vc_test = VC_app()
    vc_test.start()
