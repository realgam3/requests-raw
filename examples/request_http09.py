#!/usr/bin/env python3

import json
import requests_raw

# Added Feature https://github.com/realgam3/requests-raw/issues/5
res = requests_raw.raw(
    url='http://httpbin.org/',
    data=b"GET /get\r\n\r\n"
)
if not res.status_code:
    print(json.load(res.raw))
