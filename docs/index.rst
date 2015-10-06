rabbitmq-admin Documentation
=============================
This project is a python wrapper around the RabbitMQ Management HTTP API.
Not all API calls are supported, and the list is maintained in the project
``README.rst``.

Example
-------

.. code-block:: python

    >>> from rabbitmq_admin import AdminAPI
    >>> api = AdminAPI(url='http://192.168.99.101:15672', auth=('guest', 'guest'))
    >>> api.create_vhost('second_vhost')
    >>> api.create_user('second_user', 'password')
    >>> api.create_user_permission('second_user', 'second_vhost')
    >>> api.list_permission()
    [{'configure': '.*',
      'read': '.*',
      'user': 'guest',
      'vhost': '/',
      'write': '.*'},
     {'configure': '.*',
      'read': '.*',
      'user': 'second_user',
      'vhost': 'second_vhost',
      'write': '.*'}]


Installation
------------

To install the latest release, type::

    pip install rabbitmq-admin

To install the latest code directly from source, type::

    pip install git+git://github.com/ambitioninc/rabbitmq-admin.git
