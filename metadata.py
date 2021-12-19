# -*- coding: utf-8 -*-
"""
| *@created on:* 03/01/20,
| *@author:* Umesh Kumar,
| *@version:* v0.0.1
|
| *Description:*
| 
| *Sphinx Documentation Status:* Complete
|
"""

import json

import munch

with open('/'.join(str(__file__).split('/')[:-1]) + '/metadata.json') as f:
    metadata = munch.Munch(json.load(f))
