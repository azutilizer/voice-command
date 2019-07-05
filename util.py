import os
import re


def remove_punctuations(text):
    text = re.sub('[(;\"?!#$)]', '', text)
    return text


def read_config(cfg_file):
    ret_dict = {}
    if not os.path.exists(cfg_file):
        return ret_dict
    with open(cfg_file, 'rt') as cfg:
        for line in cfg:
            line = line.strip()
            segs = line.split(' = ')
            if len(segs) != 2:
                continue
            tmp_key = remove_punctuations(str(segs[0]))
            tmp_value = remove_punctuations(str(segs[1]))
            ret_dict[tmp_key] = tmp_value

    return ret_dict