django-fuelsdk
==============

ExactTarget FuelSDK wrapper for Django.

Install
=======

```bash
# install the custom patched version of suds
pip install -e git+https://github.com/roverdotcom/suds.git#egg=suds
# install django-fuelsdk
pip install -e git+https://github.com/roverdotcom/django-fuelsdk.git#egg=django_fuelsdk
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
