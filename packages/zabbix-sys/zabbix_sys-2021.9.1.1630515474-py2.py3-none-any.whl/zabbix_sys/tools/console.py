from __future__ import absolute_import, print_function
import json


def print_json(result):
    print(json.dumps(result, indent=2, sort_keys=True))
