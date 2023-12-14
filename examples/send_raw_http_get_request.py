#!/usr/bin/env python3

import requests_raw

res = requests_raw.raw(url='https://httpbin.org/', data=b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
res_json = res.json()
print(res_json)
