#!/usr/bin/env python3

import requests_raw

res = requests_raw.raw(
    url='https://httpbin.org/',
    data=b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n",
    proxies={
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    },
    verify=False
)
res_json = res.json()
print(res_json)
