# MIT License
#
# Copyright (c) 2017 DSX Technologies
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib.parse
import hashlib
import hmac
import time
import base64

import requests

PUBLIC_KEY = 'xxx'
SECRET_KEY = 'xxx'
DSX_URL = "https://dsx.uk/"
TRANSACTION_API_URL = urllib.parse.urljoin(DSX_URL, 'tapi/v2/')


def to_bytes(str):
    return str.encode('utf-8')


def get_signature(params_urlencoded):
    hmac_obj = hmac.new(to_bytes(SECRET_KEY), to_bytes(params_urlencoded), hashlib.sha512)
    return hmac_obj.digest()


def request(api_method, params_dict):
    params_dict['nonce'] = int(round(time.time() * 1000))
    params_urlencoded = urllib.parse.urlencode(params_dict)
    sign_bytes = get_signature(params_urlencoded)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Key': PUBLIC_KEY,
        'Sign': base64.b64encode(sign_bytes).decode('utf-8')
    }

    response = requests.post(
        urllib.parse.urljoin(TRANSACTION_API_URL, api_method),
        headers=headers,
        data=params_urlencoded
    )

    try:
        response_json = response.json()
        if response_json['success'] == 0:
            print('Received error: {}'.format(response_json['error']))
        return response_json
    except Exception as ex:
        print('Received nonsense: {}: {}'.format(response.text, ex))
        return {}


if __name__ == '__main__':
    data = request('info/account', {})
    print(data)
