# requests-raw
Use requests to send HTTP raw sockets (To Test RFC Compliance)

## Usage
```python
    import json
    import requests_raw

    res = requests_raw.raw(url='http://httpbin.org/', data=b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
    res_json = res.json()
    print(json.dumps(res_json, indent=2))
```
