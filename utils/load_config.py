import config

import json
from easydict import EasyDict as Edict


def assign_json(obj, key, value):
    if obj.get(key, None) is not None:
        if isinstance(value, dict) and (isinstance(obj[key], Edict) or isinstance(obj[key]. dict)):
            for k,v in value.iteritems():
                assign_json(obj[key], k, v)
        else:
            obj[key] = value
    else:
        obj[key] = value


def load_config(config_path='examples/config/coco.json'):
    assert isinstance(config_path, str)
    # only support json format at present
    assert config_path.endswith("json")
    with open(config_path, "r") as f:
        obj = json.load(f)
    for k,v in obj.iteritems():
        assign_json(config.__dict__, k, v)

