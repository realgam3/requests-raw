#!/usr/bin/env python3

import requests_raw

res = requests_raw.raw(url='http://httpbin.org:80/', data=open("get_request.txt", "rb").read())
res_json = res.json()
print(res_json)
