from django.test import TestCase

from mock import patch
from mock import MagicMock

from django_fuelsdk.fuel import FuelClient

from django_fuelsdk.fuel import FuelApiError
from django_fuelsdk.fuel import AlreadySubscribedError
from django_fuelsdk.fuel import NoValidSubscribersError

from django_fuelsdk.fuel import ALREADY_SUBSCRIBED_ERROR_CODE
from django_fuelsdk.fuel import NO_VALID_SUBSCRIBERS_ERROR_CODE


class FuelClientTestCase(TestCase):

    def setUp(self):
        super(FuelClientTestCase, self).setUp()
        self._et_client_patcher = patch(
            'django_fuelsdk.fuel.ConfigurableET_Client')
        self._et_client_patcher.start()
        self.addCleanup(self._et_client_patcher.stop)
        self.client = FuelClient()


class FuelClientTests(FuelClientTestCase):
    def test_build_attributes(self):
        data = {'key': 'value'}
        self.assertEqual(
            self.client.build_attributes(data),
            [{'Name': 'key', 'Value': 'value'}])

    def test_process_result_success(self):
        response = MagicMock()
        response.message = 'OK'

        self.assertEqual(
            self.client.process_result(response),
            response)

    def test_process_result_failure_raises_exception(self):
        response = MagicMock()
        response.message = 'Error'

        with self.assertRaises(FuelApiError):
            self.client.process_result(response)


class FuelClientEtMockTestCase(FuelClientTestCase):
    def setUp(self):
        super(FuelClientEtMockTestCase, self).setUp()
        self._et_patcher = patch(self.et_patch_location)
        class_mock = self._et_patcher.start()
        self.addCleanup(self._et_patcher.stop)

        self.instance = MagicMock()
        class_mock.return_value = self.instance

        self.response = MagicMock()
        self.response.message = 'OK'


class FuelClientSendTests(FuelClientEtMockTestCase):
    et_patch_location = 'django_fuelsdk.fuel.ET_TriggeredSend'

    def setUp(self):
        super(FuelClientSendTests, self).setUp()
        self.instance.send.return_value = self.response

    def send(self):
        self.client.send(
            'Test Email', 'test@example.com', {'First Name': 'Bob'})

    def test_calls_send(self):
        self.send()
        self.assertTrue(self.instance.send.called)

    def test_sets_props(self):
        self.send()
        self.assertEqual(
            self.instance.props,
            {'CustomerKey': 'Test Email'})

    def test_sets_subcribers(self):
        self.send()
        self.assertEqual(
            self.instance.subscribers,
            [{
                'EmailAddress': 'test@example.com',
                'SubscriberKey': 'test@example.com',
                'Attributes': [{'Name': 'First Name', 'Value': 'Bob'}],
            }])

    def test_raises_on_no_valid_subscribers(self):
        self.response.message = 'Error'
        self.response.results = [
            {'ErrorCode': NO_VALID_SUBSCRIBERS_ERROR_CODE}
        ]
        with self.assertRaises(NoValidSubscribersError):
            self.send()

    def test_error_still_raised_on_strange_response(self):
        self.response.message = 'Error'
        self.response.results = []
        with self.assertRaises(FuelApiError):
            self.send()


class FuelClientAddSubscriberTests(FuelClientEtMockTestCase):
    et_patch_location = 'django_fuelsdk.fuel.ET_Subscriber'

    def setUp(self):
        super(FuelClientAddSubscriberTests, self).setUp()
        self.instance.post.return_value = self.response

    def add_subscriber(self):
        self.client.add_subscriber('test@example.com', {'First Name': 'Bob'})

    def test_calls_post(self):
        self.add_subscriber()
        self.assertTrue(self.instance.post.called)

    def test_sets_props(self):
        self.add_subscriber()
        self.assertEqual(
            self.instance.props,
            {
                'EmailAddress': 'test@example.com',
                'SubscriberKey': 'test@example.com',
                'Attributes': [{'Name': 'First Name', 'Value': 'Bob'}],
            })

    def test_raises_on_already_subscribed(self):
        self.response.message = 'Error'
        self.response.results = [{'ErrorCode': ALREADY_SUBSCRIBED_ERROR_CODE}]
        with self.assertRaises(AlreadySubscribedError):
            self.add_subscriber()

    def test_error_still_raised_on_strange_response(self):
        self.response.message = 'Error'
        self.response.results = []
        with self.assertRaises(FuelApiError):
            self.add_subscriber()
