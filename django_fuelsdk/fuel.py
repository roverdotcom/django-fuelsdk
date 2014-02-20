from django.core import mail

from FuelSDK import ET_TriggeredSend
from FuelSDK import ET_Subscriber

from django_fuelsdk.client import ConfigurableET_Client
from django_fuelsdk.constants import CLIENT_ID
from django_fuelsdk.constants import CLIENT_SECRET
from django_fuelsdk.constants import WSDL_URL


class FuelApiError(StandardError):
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
        if response.message != 'OK':
            raise FuelApiError('API error: %s' % response.results)

        return response

    def send(self, email, to, data):
        ts = ET_TriggeredSend()
        ts.auth_stub = self.client
        ts.props = {'CustomerKey': email}
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
        return self.process_result(sub.post())


class DebugFuelClient(object):
    def send(self, email, to, data):
        print 'Email %s sent to %s with the data %s' % (email, to, data)

    def add_subscriber(self, email_address, data):
        print 'Subscriber %s added with the data %s' % (email_address, data)


class TestFuelClient(object):
    def send(self, email, to, data):
        mail.outbox.append({
            'email': email,
            'to': to,
            'data': data,
        })
