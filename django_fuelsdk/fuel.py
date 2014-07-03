from django.core import mail

from FuelSDK import ET_TriggeredSend
from FuelSDK import ET_Subscriber

from django_fuelsdk.client import ConfigurableET_Client
from django_fuelsdk.constants import CLIENT_ID
from django_fuelsdk.constants import CLIENT_SECRET
from django_fuelsdk.constants import WSDL_URL


ALREADY_SUBSCRIBED_ERROR_CODE = 12014
NO_VALID_SUBSCRIBERS_ERROR_CODE = 180008


class FuelApiError(StandardError):
    def __init__(self, results):
        self.results = results

    def __unicode__(self):
        return repr(self.results)

    def __str__(self):
        return unicode(self)


class AlreadySubscribedError(FuelApiError):
    pass


class NoValidSubscribersError(FuelApiError):
    pass


class FuelClient(object):
    def __init__(self):
        self.client = ConfigurableET_Client(
            CLIENT_ID,
            CLIENT_SECRET,
            wsdl_server_url=WSDL_URL)

    def build_attributes(self, data):
        return [{'Name': key, 'Value': value} for key, value in data.items()]

    def process_result(self, response):
        try:
            if response.message == 'Error':
                error_code = response.results[0]['ErrorCode']
                if error_code == ALREADY_SUBSCRIBED_ERROR_CODE:
                    raise AlreadySubscribedError(response.results)
                elif error_code == NO_VALID_SUBSCRIBERS_ERROR_CODE:
                    raise NoValidSubscribersError(response.results)

        except (IndexError, KeyError):
            # In case of error continue with normal error processing
            pass

        if response.message != 'OK':
            raise FuelApiError(response.results)

        return response

    def send(self, email_name, to, data):
        ts = ET_TriggeredSend()
        ts.auth_stub = self.client
        ts.props = {'CustomerKey': email_name}
        ts.subscribers = [{
            'EmailAddress': to,
            'SubscriberKey': to,
            'Attributes': self.build_attributes(data),
        }]
        return self.process_result(ts.send())

    def add_subscriber(self, email_address, data):
        sub = ET_Subscriber()
        sub.auth_stub = self.client
        sub.props = {
            'EmailAddress': email_address,
            'SubscriberKey': email_address,
            'Attributes': self.build_attributes(data)
        }
        response = sub.post()
        return self.process_result(response)


class DebugFuelClient(object):
    def send(self, email_name, to, data=None):
        print 'Email %s sent to %s with the data %s' % (email_name, to, data)

    def add_subscriber(self, email_address, data=None):
        print 'Subscriber %s added with the data %s' % (email_address, data)


class ExactTargetEmail(object):
    def __init__(self, email, to, context_data):
        self.email = email
        self.to = to
        self.context_data = context_data


class TestFuelClient(object):
    def send(self, email, to, data):
        mail.outbox.append(ExactTargetEmail(email, to, data))
