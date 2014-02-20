django-fuelsdk
==============

ExactTarget FuelSDK wrapper for Django.

.. image:: https://travis-ci.org/bradjasper/django-jsonfield.png?branch=master

Install
=======

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Add To INSTALLED_APPS**
```python
INSTALLED_APPS = [
    # ...
    django_fuelsdk,
]
```

**Add Settings**
```python
EXACT_TARGET_CLIENT_ID = 'xxxx'
EXACT_TARGET_CLIENT_SECRET = 'xxxx'
# https://code.exacttarget.com/question/there-any-cetificrate-install-our-server-access-et-api
EXACT_TARGET_WSDL_URL = 'https://webservice.exacttarget.com/etframework.wsdl'
```


Usage
=====

```python
from django_fuelsdk.fuel import FuelClient

f = FuelClient()

r = f.send('Welcome', 'test@example.com', {'variable': 'test'})
```
