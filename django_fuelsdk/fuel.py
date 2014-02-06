from FuelSDK import ET_TriggeredSend

from client import ConfigurableET_Client


class FuelClient(object):
    def __init__(self, *args, **kwargs):
        self.client = ConfigurableET_Client(*args, **kwargs)

    def build_attributes(self, data):
        return [{'Name': key, 'Value': value} for key, value in data.items()]

    def send(self, email, to, data):
        ts = ET_TriggeredSend()
        ts.auth_stub = self.client
        ts.props = {'CustomerKey': email}
        ts.subscribers = [{
            'EmailAddress': to,
            'SubscriberKey': to,
            'Attributes': self.build_attributes(data),
        }]
        return ts.send()
