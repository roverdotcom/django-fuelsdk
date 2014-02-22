django-fuelsdk
==============

ExactTarget FuelSDK wrapper for Django.

![Travis CI Build Status](https://travis-ci.org/bradjasper/django-jsonfield.png?branch=master)

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

# Send a triggered send to a specific subscriber (used for transactional email)
f.send('Welcome', 'test@example.com', {'variable': 'test'})

# Add a subscriber
# Note: The underlying ExactTarget API throws an error when trying to
# add a subscriber that already exists. This method will silence that error,
# making add_subscriber idempotent. 
f.add_subscriber('test@example.com', {'variable': 'test'})

# Any error returned by the API will cause a django_fuelsdk.fuel.FuelApiError
# exception to be raised. 
f.send('Not an Email', 'test@example.com', {})
```
