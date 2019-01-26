# -*- coding:utf-8 -*-
import wechatsogou
import json
import os
from hashlib import md5
import traceback
import requests


class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.base_params = {
            'username': username,
            'password': md5(password.encode('utf-8')).hexdigest(),
            'softid': soft_id,
            'softkey': soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, img_byte, im_type, timeout=60):
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        files = {'image': ('code.jpg', img_byte)}
        print(files)
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/create.json', data=params, headers=self.headers, files=files)
        return r.json()

    def rk_report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


def identify_image_callback(img, code="3000"):
    try:
        username = 'twenty1997'
        password = 'qwertyuiop'
        id_ = '1'
        key = 'b40ffbee5c1cf4e38028c197eb2fc751'
        rc = RClient(username, password, id_, key)
        result = rc.rk_create(img, code)
        print(json.dumps(result).decode('unicode-escape'))
        global count
        count = count + 1
        print(count)
        return result['Result']
    except Exception as e:
        print(traceback.format_exc())

    
    