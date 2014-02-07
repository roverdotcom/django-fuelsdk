django-fuelsdk
==============

ExactTarget FuelSDK wrapper for Django.

Install
=======

```bash
pip install -r requirements.txt
```

Usage
=====

```python
from django_fuelsdk.fuel import FuelClient

f = FuelClient(
    client_id='xxxxxx',
    client_secret='xxxxxxx',
    wsdl_server_url='https://webservice.s6.exacttarget.com/etframework.wsdl')

r = f.send('Welcome', 'test@example.com', {'variable': 'test'})
```
