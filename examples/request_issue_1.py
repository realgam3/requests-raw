#!/usr/bin/env python3

import requests_raw

res = requests_raw.raw(
    url="https://www.google.com",
    data=b"GET /?ani=asas HTTP/1.1\r\nHost: www.google.com\r\nUser-Agent: Mozilla Firefox 55/66\r\n\r\n"
)
print(res.content)
