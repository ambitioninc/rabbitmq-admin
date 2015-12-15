from unittest import TestCase

from mock import patch, Mock
import requests

from rabbitmq_admin.base import Resource


class ResourceTests(TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:15672'
        self.auth = ('guest', 'guest')
        self.verify = True

        self.resource = Resource(self.url, self.auth, self.verify)

    def test_init(self):
        resource = Resource(self.url, self.auth, self.verify)

        self.assertEqual(resource.url, self.url)
        self.assertEqual(resource.session.auth, self.auth)
        self.assertEqual(resource.session.verify, self.verify)
        self.assertDictContainsSubset(
            {'Content-type': 'application/json'},
            resource.session.headers
        )

    @patch.object(requests.Session, 'put', autospec=True)
    def test_put_no_data(self, mock_put):

        mock_response = Mock()
        mock_put.return_value = mock_response

        self.resource._put(self.url, auth=self.auth)

        mock_response.raise_for_status.assert_called_once_with()

    @patch.object(Resource, '_post')
    def test_api_post(self, mock_post):
        url = '/api/definitions'
        headers = {'k1': 'v1'}

        self.resource._api_post(url, headers=headers)
        mock_post.assert_called_once_with(
            url=self.url + url,
            headers={'k1': 'v1'}
        )

    @patch.object(requests.Session, 'post', autospec=True)
    def test_post_no_data(self, mock_post):

        mock_response = Mock()
        mock_post.return_value = mock_response

        self.resource._post(self.url, auth=self.auth)

        mock_response.raise_for_status.assert_called_once_with()

    @patch.object(requests.Session, 'post', autospec=True)
    def test_post(self, mock_post):

        mock_response = Mock()
        mock_post.return_value = mock_response

        self.resource._post(self.url, auth=self.auth, data={'hello': 'world'})

        mock_response.raise_for_status.assert_called_once_with()
