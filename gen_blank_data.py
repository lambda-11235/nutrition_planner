#!/usr/bin/env python3

import argparse
import glob
import json

from data import *

parser = argparse.ArgumentParser(
    description="generate a blank ingredient template")
parser.add_argument('name', type=str,
    help="")
parser.add_argument('--json-indent', type=int, default=2,
    help="indent on JSON blocks (default %(default)s)")
args = parser.parse_args()

d = Data()
d.name = args.name
print(json.dumps(d.encode(), indent=args.json_indent))
