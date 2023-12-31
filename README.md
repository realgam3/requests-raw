# requests-raw
[![PyPI version](https://img.shields.io/pypi/v/requests-raw)](https://pypi.org/project/requests-raw/)
[![Downloads](https://pepy.tech/badge/requests-raw)](https://pepy.tech/project/requests-raw)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requests-raw)  

Use [requests](https://requests.readthedocs.io/) to send HTTP raw sockets (To Test RFC Compliance)

![Logo](https://raw.githubusercontent.com/realgam3/requests-raw/v2.0.0/ext/requests-raw-logo.png)

## Usage
```python
import json
import requests_raw


res = requests_raw.raw(url='http://httpbin.org/', data=b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
res_json = res.json()
print(json.dumps(res_json, indent=2))
```

## Installation
### Prerequisites
* Python 3.7+

```sh
pip3 install requests-raw
```
