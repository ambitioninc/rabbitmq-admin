import os
from unittest import TestCase

import pika
import requests

from rabbitmq_admin.api import AdminAPI


class AdminAPITests(TestCase):
    """
    These test cases require a docker container up and running
    ::

        docker run -d \
            -h rabbit1 \
            -p 5672:5672 \
            -p 15672:15672 \
            -e RABBITMQ_DEFAULT_USER=guest \
            -e RABBITMQ_DEFAULT_PASS=guest \
            -name rabbit1 \
            rabbitmq:3-management

    """

    @classmethod
    def setUpClass(cls):
        """
        One-time set up that connects as 'guest', creates a 'test_queue' and
        sends one message
        """
        if os.environ.get('TRAVIS'):  # pragma: no cover
            cls.host = '127.0.0.1'
        else:  # pragma: no cover
            cls.host = os.environ.get('RABBITMQ_HOST', '192.168.99.101')

        credentials = pika.PlainCredentials('guest', 'guest')
        cls.connection = pika.BlockingConnection(
            pika.ConnectionParameters(cls.host, credentials=credentials),
        )
        channel = cls.connection.channel()
        channel.queue_declare(queue='test_queue')
        channel.basic_publish(
            exchange='',
            routing_key='test_queue',
            body='Test Message')

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        super(AdminAPITests, self).setUp()

        url = 'http://{host}:15672'.format(host=self.host)

        self.api = AdminAPI(url, auth=('guest', 'guest'))
        self.node_name = 'rabbit@rabbit1'

    def test_overview(self):
        response = self.api.overview()
        self.assertIsInstance(response, dict)

    def test_get_cluster_name(self):
        self.assertDictEqual(
            self.api.get_cluster_name(),
            {'name': 'rabbit@rabbit1'}
        )

    def test_list_nodes(self):
        self.assertEqual(
            len(self.api.list_nodes()),
            1
        )

    def test_get_node(self):
        response = self.api.get_node(self.node_name)
        self.assertIsInstance(response, dict)
        self.assertEqual(response['name'], self.node_name)

    def test_list_extensions(self):
        self.assertEqual(
            self.api.list_extensions(),
            [{'javascript': 'dispatcher.js'}]
        )

    def test_list_connections(self):
        self.assertEqual(
            len(self.api.list_connections()),
            1
        )

    def test_get_connection(self):
        cname = self.api.list_connections()[0].get('name')
        self.assertIsInstance(
            self.api.get_connection(cname),
            dict
        )

    def test_delete_connection(self):
        with self.assertRaises(requests.HTTPError):
            self.api.delete_connection('not-a-connection')

    def test_delete_connection_with_reson(self):
        with self.assertRaises(requests.HTTPError):
            self.api.delete_connection('not-a-connection', 'I don\'t like you')

    def test_list_connection_channels(self):
        cname = self.api.list_connections()[0].get('name')
        response = self.api.list_connection_channels(cname)

        self.assertEqual(
            response[0].get('name'),
            cname + ' (1)'
        )

    def test_list_channels(self):
        self.assertEqual(
            len(self.api.list_channels()),
            1
        )

    def test_get_channel(self):
        cname = self.api.list_channels()[0].get('name')
        self.assertIsInstance(
            self.api.get_channel(cname),
            dict
        )

    def test_list_consumers(self):
        self.assertEqual(
            self.api.list_consumers(),
            []
        )

    def test_list_consumers_for_vhost(self):
        self.assertEqual(
            self.api.list_consumers_for_vhost('/'),
            []
        )

    def test_list_exchanges(self):
        self.assertEqual(
            len(self.api.list_exchanges()),
            8
        )

    def test_list_exchanges_for_vhost(self):
        self.assertEqual(
            len(self.api.list_exchanges_for_vhost('/')),
            8
        )

    def test_get_create_delete_exchange_for_vhost(self):
        name = 'myexchange'
        body = {
            "type": "direct",
            "auto_delete": False,
            "durable": False,
            "internal": False,
            "arguments": {}
        }

        self.api.create_exchange_for_vhost(name, '/', body)
        self.assertEqual(
            len(self.api.list_exchanges_for_vhost('/')),
            9
        )
        self.assertEqual(
            self.api.get_exchange_for_vhost(name, '/').get('name'),
            name
        )

        self.api.delete_exchange_for_vhost(name, '/')
        self.assertEqual(
            len(self.api.list_exchanges_for_vhost('/')),
            8
        )

    def test_list_bindings(self):
        self.assertEqual(
            self.api.list_bindings(),
            [{'arguments': {},
              'destination': 'aliveness-test',
              'destination_type': 'queue',
              'properties_key': 'aliveness-test',
              'routing_key': 'aliveness-test',
              'source': '',
              'vhost': '/'},
             {'arguments': {},
              'destination': 'test_queue',
              'destination_type': 'queue',
              'properties_key': 'test_queue',
              'routing_key': 'test_queue',
              'source': '',
              'vhost': '/'}]
        )

    def test_list_bindings_for_vhost(self):
        self.assertEqual(
            self.api.list_bindings_for_vhost('/'),
            [{'arguments': {},
              'destination': 'aliveness-test',
              'destination_type': 'queue',
              'properties_key': 'aliveness-test',
              'routing_key': 'aliveness-test',
              'source': '',
              'vhost': '/'},
             {'arguments': {},
              'destination': 'test_queue',
              'destination_type': 'queue',
              'properties_key': 'test_queue',
              'routing_key': 'test_queue',
              'source': '',
              'vhost': '/'}]
        )

    def test_list_vhosts(self):
        response = self.api.list_vhosts()
        self.assertEqual(
            len(response),
            1
        )
        self.assertEqual(response[0].get('name'), '/')

    def test_get_vhosts(self):
        response = self.api.get_vhost('/')
        self.assertEqual(response.get('name'), '/')

    def test_create_delete_vhost(self):
        name = 'vhost2'

        self.api.create_vhost(name)
        self.assertEqual(
            len(self.api.list_vhosts()),
            2
        )

        self.api.delete_vhost(name)
        self.assertEqual(
            len(self.api.list_vhosts()),
            1
        )

    def test_create_delete_vhost_tracing(self):
        name = 'vhost2'

        self.api.create_vhost(name, tracing=True)
        self.assertEqual(
            len(self.api.list_vhosts()),
            2
        )

        self.api.delete_vhost(name)
        self.assertEqual(
            len(self.api.list_vhosts()),
            1
        )

    def test_list_users(self):
        self.assertEqual(
            len(self.api.list_users()),
            1
        )

    def test_get_user(self):
        response = self.api.get_user('guest')
        self.assertEqual(response.get('name'), 'guest')
        self.assertEqual(response.get('tags'), 'administrator')

    def test_create_delete_user(self):
        name = 'user2'
        password_hash = '5f4dcc3b5aa765d61d8327deb882cf99'  # md5 of 'password'

        self.api.create_user(name, password='', password_hash=password_hash)
        self.assertEqual(
            len(self.api.list_users()),
            2
        )

        self.api.delete_user(name)
        self.assertEqual(
            len(self.api.list_users()),
            1
        )

    def test_create_delete_user_password(self):
        name = 'user2'
        password = 'password'

        self.api.create_user(name, password=password)
        self.assertEqual(
            len(self.api.list_users()),
            2
        )

        self.api.delete_user(name)
        self.assertEqual(
            len(self.api.list_users()),
            1
        )

    def test_create_delete_user_no_password(self):
        name = 'user2'
        password = ''

        self.api.create_user(name, password=password)
        self.assertEqual(
            len(self.api.list_users()),
            2
        )

        self.api.delete_user(name)
        self.assertEqual(
            len(self.api.list_users()),
            1
        )

    def test_list_user_permissions(self):
        self.assertEqual(
            self.api.list_user_permissions('guest'),
            [{'configure': '.*',
              'read': '.*',
              'user': 'guest',
              'vhost': '/',
              'write': '.*'}]
        )

    def test_whoami(self):
        self.assertEqual(
            self.api.whoami(),
            {'name': 'guest', 'tags': 'administrator'}
        )

    def test_list_permissions(self):
        self.assertEqual(
            self.api.list_permissions(),
            [{'configure': '.*',
              'read': '.*',
              'user': 'guest',
              'vhost': '/',
              'write': '.*'}]
        )

    def test_get_user_permission(self):
        self.assertEqual(
            self.api.get_user_permission('/', 'guest'),
            {
                'configure': '.*',
                'read': '.*',
                'user': 'guest',
                'vhost': '/',
                'write': '.*'
            }
        )

    def test_create_delete_user_permission(self):
        uname = 'test_user'
        vname = 'test_vhost'
        password_hash = '5f4dcc3b5aa765d61d8327deb882cf99'  # md5 of 'password'

        # Create test user/vhost
        self.api.create_user(uname, password='', password_hash=password_hash)
        self.api.create_vhost(vname)

        self.assertEqual(len(self.api.list_user_permissions(uname)), 0)

        # Create the permission
        self.api.create_user_permission(uname, vname)

        self.assertEqual(len(self.api.list_user_permissions(uname)), 1)

        # Delete the permission
        self.api.delete_user_permission(uname, vname)

        self.assertEqual(len(self.api.list_user_permissions(uname)), 0)
        # delete test user/vhost
        self.api.delete_user(uname)
        self.api.delete_vhost(vname)

    def test_is_vhost_alive(self):
        self.assertDictEqual(
            self.api.is_vhost_alive('/'),
            {'status': 'ok'}
        )
