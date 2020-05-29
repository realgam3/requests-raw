# requests-raw
[![PyPI version](https://img.shields.io/pypi/v/requests-raw)](https://pypi.org/project/requests-raw/)
[![Downloads](https://pepy.tech/badge/requests-raw)](https://pepy.tech/project/requests-raw)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requests-raw)  

Use [requests](https://requests.readthedocs.io/) to send HTTP raw sockets (To Test RFC Compliance)

## Usage
### Explicit
```python
import json
import requests_raw

res = requests_raw.raw(url='http://httpbin.org/', data=b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
res_json = res.json()
print(json.dumps(res_json, indent=2))
```

### Implicit (monkey patch)
```python
import json
import requests
import requests_raw
requests_raw.monkey_patch_all()

session = requests.Session()
res = session.raw(url='https://httpbin.org/', data=b"GET /cookies/set/name/value HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
res_json = res.json()
print(json.dumps(res_json, indent=2))
```

## Installation
### Prerequisites
* Python 2.7
* Python 3.5+

```sh
pip3 install requests-raw
```
