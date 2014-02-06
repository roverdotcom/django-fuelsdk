from django.core import mail

from FuelSDK import ET_TriggeredSend

from client import ConfigurableET_Client


class FuelApiError(StandardError):
    pass


class FuelClientBase(object):
    def __init__(self):
        raise NotImplemented()

    def send(self, email, to, data):
        raise NotImplemented()


class FuelClient(FuelClientBase):
    def __init__(self, *args, **kwargs):
        self.client = ConfigurableET_Client(*args, **kwargs)

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


class DebugFuelClient(FuelClientBase):
    def __init__(self, *args, **kwargs):
        pass

    def send(self, email, to, data):
        print 'Email %s sent to %s with the data %s' % (email, to, data)


class TestFuelClient(FuelClientBase):
    def __init__(self, *args, **kwargs):
        pass

    def send(self, email, to, data):
        mail.outbox.append({
            'email': email,
            'to': to,
            'data': data,
        })
