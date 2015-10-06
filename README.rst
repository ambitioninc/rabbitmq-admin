.. image:: https://travis-ci.org/ambitioninc/rabbitmq-admin.png
   :target: https://travis-ci.org/ambitioninc/rabbitmq-admin

.. image:: https://coveralls.io/repos/ambitioninc/rabbitmq-admin/badge.png?branch=develop
    :target: https://coveralls.io/r/ambitioninc/rabbitmq-admin?branch=develop


rabbitmq-admin
==============
This project is a python wrapper around the RabbitMQ Management HTTP API.


Example
-------
::

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

Unsupported Management API endpoints
------------------------------------
This is a list of unsupported API endpoints. Please do not make issues for
these, but pull requests implementing them are welcome.

- ``/api/definitions [GET, POST]``
- ``/api/exchanges/vhost/name/bindings/source [GET]``
- ``/api/exchanges/vhost/name/bindings/destination [GET]``
- ``/api/exchanges/vhost/name/publish [POST]``
- ``/api/queues/vhost/name/bindings [GET]``
- ``/api/queues/vhost/name/contents [DELETE]``
- ``/api/queues/vhost/name/actions [POST]``
- ``/api/queues/vhost/name/get [POST]``
- ``/api/bindings/vhost/e/exchange/q/queue [GET, POST]``
- ``/api/bindings/vhost/e/exchange/q/queue/props [GET, DELETE]``
- ``/api/bindings/vhost/e/source/e/destination [GET, POST]``
- ``/api/bindings/vhost/e/source/e/destination/props [GET, DELETE]``
- ``/api/parameters [GET]``
- ``/api/parameters/component [GET]``
- ``/api/parameters/component/vhost [GET]``
- ``/api/parameters/component/vhost/name [GET, PUT, DELETE]``
- ``/api/policies [GET]``
- ``/api/policies/vhost [GET]``
- ``/api/policies/vhost/name [GET, PUT, DELETE]``

Installation
------------
To install the latest release, type::

    pip install rabbitmq-admin

To install the latest code directly from source, type::

    pip install git+git://github.com/ambitioninc/rabbitmq-admin.git

Documentation
-------------
Full documentation is available at http://rabbitmq-admin.readthedocs.org

License
-------
MIT License (see LICENSE)
