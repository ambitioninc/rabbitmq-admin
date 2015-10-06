from rabbitmq_admin.base import Resource
from six.moves import urllib


class AdminAPI(Resource):
    """
    The entrypoint for interacting with the RabbitMQ Management HTTP API
    """

    def overview(self):
        """
        Various random bits of information that describe the whole system
        """
        return self._get(
            url=self.url + '/api/overview',
            headers=self.headers,
            auth=self.auth
        )

    def get_cluster_name(self):
        """
        Name identifying this RabbitMQ cluster.
        """
        return self._get(
            url=self.url + '/api/cluster-name',
            headers=self.headers,
            auth=self.auth
        )

    def list_nodes(self):
        """
        A list of nodes in the RabbitMQ cluster.
        """
        return self._get(
            url=self.url + '/api/nodes',
            headers=self.headers,
            auth=self.auth
        )

    def get_node(self, name, memory=False, binary=False):
        """
        An individual node in the RabbitMQ cluster. Set "memory=true" to get
        memory statistics, and "binary=true" to get a breakdown of binary
        memory use (may be expensive if there are many small binaries in the
        system).
        """

        url = self.url + '/api/nodes/{0}'.format(name)

        return self._get(
            url=url,
            params=dict(
                binary=binary,
                memory=memory,
            ),
            headers=self.headers,
            auth=self.auth
        )

    def list_extensions(self):
        """
        A list of extensions to the management plugin.
        """
        return self._get(
            url=self.url + '/api/extensions',
            headers=self.headers,
            auth=self.auth
        )

    def list_connections(self):
        """
        A list of all open connections.
        """
        return self._get(
            url=self.url + '/api/connections',
            headers=self.headers,
            auth=self.auth
        )

    def get_connection(self, name):
        """
        An individual connection.

        :param name: The connection name
        :type name: str
        """
        return self._get(
            url=self.url + '/api/connections/{0}'.format(
                urllib.parse.quote_plus(name)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def delete_connection(self, name, reason=None):
        """
        Closes an individual connection. Give an optional reason

        :param name: The connection name
        :type name: str

        :param reason: An option reason why the connection was deleted
        :type reason: str
        """
        headers = self.headers.copy()
        if reason:
            headers['X-Reason'] = reason

        self._delete(
            url=self.url + '/api/connections/{0}'.format(
                urllib.parse.quote_plus(name)
            ),
            headers=headers,
            auth=self.auth
        )

    def list_connection_channels(self, name):
        """
        List of all channels for a given connection.

        :param name: The connection name
        :type name: str
        """
        return self._get(
            url=self.url + '/api/connections/{0}/channels'.format(
                urllib.parse.quote_plus(name)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def list_channels(self):
        """
        A list of all open channels.
        """
        return self._get(
            url=self.url + '/api/channels',
            headers=self.headers,
            auth=self.auth
        )

    def get_channel(self, name):
        """
        Details about an individual channel.

        :param name: The channel name
        :type name: str
        """
        return self._get(
            url=self.url + '/api/channels/{0}'.format(
                urllib.parse.quote_plus(name)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def list_consumers(self):
        """
        A list of all consumers.
        """
        return self._get(
            url=self.url + '/api/consumers',
            headers=self.headers,
            auth=self.auth
        )

    def list_consumers_for_vhost(self, vhost):
        """
        A list of all consumers in a given virtual host.

        :param vhost: The vhost name
        :type vhost: str
        """
        return self._get(
            url=self.url + '/api/consumers/{0}'.format(
                urllib.parse.quote_plus(vhost)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def list_exchanges(self):
        """
        A list of all exchanges.
        """
        return self._get(
            url=self.url + '/api/exchanges',
            headers=self.headers,
            auth=self.auth
        )

    def list_exchanges_for_vhost(self, vhost):
        """
        A list of all exchanges in a given virtual host.

        :param vhost: The vhost name
        :type vhost: str
        """
        return self._get(
            url=self.url + '/api/exchanges/{0}'.format(
                urllib.parse.quote_plus(vhost)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def get_exchange_for_vhost(self, exchange, vhost):
        """
        An individual exchange

        :param exchange: The exchange name
        :type exchange: str

        :param vhost: The vhost name
        :type vhost: str
        """
        return self._get(
            url=self.url + '/api/exchanges/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(exchange)),
            headers=self.headers,
            auth=self.auth
        )

    def create_exchange_for_vhost(self, exchange, vhost, body):
        """
        Create an individual exchange.
        The body should look like:
        ::

            {
                "type": "direct",
                "auto_delete": false,
                "durable": true,
                "internal": false,
                "arguments": {}
            }

        The type key is mandatory; other keys are optional.

        :param exchange: The exchange name
        :type exchange: str

        :param vhost: The vhost name
        :type vhost: str

        :param body: A body for the exchange.
        :type body: dict
        """
        self._put(
            url=self.url + '/api/exchanges/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(exchange)),
            headers=self.headers,
            auth=self.auth,
            data=body
        )

    def delete_exchange_for_vhost(self, exchange, vhost, if_unused=False):
        """
        Delete an individual exchange. You can add the parameter
        ``if_unused=True``. This prevents the delete from succeeding if the
        exchange is bound to a queue or as a source to another exchange.

        :param exchange: The exchange name
        :type exchange: str

        :param vhost: The vhost name
        :type vhost: str

        :param if_unused: Set to ``True`` to only delete if it is unused
        :type if_unused: bool
        """
        self._delete(
            url=self.url + '/api/exchanges/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(exchange)),
            params={
                'if-unused': if_unused
            },
            headers=self.headers,
            auth=self.auth
        )

    def list_bindings(self):
        """
        A list of all bindings.
        """
        return self._get(
            url=self.url + '/api/bindings',
            headers=self.headers,
            auth=self.auth
        )

    def list_bindings_for_vhost(self, vhost):
        """
        A list of all bindings in a given virtual host.

        :param vhost: The vhost name
        :type vhost: str
        """
        return self._get(
            url=self.url + '/api/bindings/{}'.format(
                urllib.parse.quote_plus(vhost)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def list_vhosts(self):
        """
        A list of all vhosts.
        """
        return self._get(
            url=self.url + '/api/vhosts',
            headers=self.headers,
            auth=self.auth
        )

    def get_vhost(self, name):
        """
        Details about an individual vhost.

        :param name: The vhost name
        :type name: str
        """
        return self._get(
            url=self.url + '/api/vhosts/{0}'.format(urllib.parse.quote_plus(name)),
            headers=self.headers,
            auth=self.auth
        )

    def delete_vhost(self, name):
        """
        Delete a vhost.

        :param name: The vhost name
        :type name: str
        """
        self._delete(
            url=self.url + '/api/vhosts/{0}'.format(urllib.parse.quote_plus(name)),
            headers=self.headers,
            auth=self.auth
        )

    def create_vhost(self, name, tracing=False):
        """
        Create an individual vhost.

        :param name: The vhost name
        :type name: str

        :param tracing: Set to ``True`` to enable tracing
        :type tracing: bool
        """
        data = {}
        if tracing:
            data['tracing'] = True
        self._put(
            url=self.url + '/api/vhosts/{0}'.format(urllib.parse.quote_plus(name)),
            headers=self.headers,
            auth=self.auth,
            data=data,
        )

    def list_users(self):
        """
        A list of all users.
        """
        return self._get(
            url=self.url + '/api/users',
            headers=self.headers,
            auth=self.auth
        )

    def get_user(self, name):
        """
        Details about an individual user.

        :param name: The user's name
        :type name: str
        """
        return self._get(
            url=self.url + '/api/users/{0}'.format(urllib.parse.quote_plus(name)),
            headers=self.headers,
            auth=self.auth
        )

    def delete_user(self, name):
        """
        Delete a user.

        :param name: The user's name
        :type name: str
        """
        self._delete(
            url=self.url + '/api/users/{0}'.format(urllib.parse.quote_plus(name)),
            headers=self.headers,
            auth=self.auth
        )

    def create_user(self, name, password, password_hash=None, tags=None):
        """
        Create a user

        :param name: The user's name
        :type name: str
        :param password: The user's password. Set to "" if no password is
            desired. Takes precedence if ``password_hash`` is also set.
        :type password: str
        :param password_hash: An optional password hash for the user.
        :type password_hash: str
        :param tags: A list of tags for the user. Currently recognised tags are
            "administrator", "monitoring" and "management". If no tags are
            supplied, the user will have no permissions.
        :type tags: list of str
        """
        data = {
            'tags': ', '.join(tags or [])
        }
        if password:
            data['password'] = password
        elif password_hash:
            data['password_hash'] = password_hash
        else:
            data['password_hash'] = ""

        self._put(
            url=self.url + '/api/users/{0}'.format(urllib.parse.quote_plus(name)),
            headers=self.headers,
            auth=self.auth,
            data=data,
        )

    def list_user_permissions(self, name):
        """
        A list of all permissions for a given user.

        :param name: The user's name
        :type name: str
        """
        return self._get(
            url=self.url + '/api/users/{0}/permissions'.format(urllib.parse.quote_plus(name)),
            headers=self.headers,
            auth=self.auth
        )

    def whoami(self):
        """
        Details of the currently authenticated user.
        """
        return self._get(
            url=self.url + '/api/whoami',
            headers=self.headers,
            auth=self.auth
        )

    def list_permissions(self):
        """
        A list of all permissions for all users.
        """
        return self._get(
            url=self.url + '/api/permissions',
            headers=self.headers,
            auth=self.auth
        )

    def get_user_permission(self, vhost, name):
        """
        An individual permission of a user and virtual host.

        :param vhost: The vhost name
        :type vhost: str

        :param name: The user's name
        :type name: str
        """
        return self._get(
            url=self.url + '/api/permissions/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(name)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def delete_user_permission(self, name, vhost):
        """
        Delete an individual permission of a user and virtual host.

        :param name: The user's name
        :type name: str

        :param vhost: The vhost name
        :type vhost: str
        """
        self._delete(
            url=self.url + '/api/permissions/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(name)
            ),
            headers=self.headers,
            auth=self.auth
        )

    def create_user_permission(self,
                               name,
                               vhost,
                               configure=None,
                               write=None,
                               read=None):
        """
        Create a user permission
        :param name: The user's name
        :type name: str
        :param vhost: The vhost to assign the permission to
        :type vhost: str

        :param configure: A regex for the user permission. Default is ``.*``
        :type configure: str
        :param write: A regex for the user permission. Default is ``.*``
        :type write: str
        :param read: A regex for the user permission. Default is ``.*``
        :type read: str
        """
        data = {
            'configure': configure or '.*',
            'write': write or '.*',
            'read': read or '.*',
        }

        self._put(
            url=self.url + '/api/permissions/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(name)
            ),
            headers=self.headers,
            auth=self.auth,
            data=data,
        )

    def is_vhost_alive(self, vhost):
        """
        Declares a test queue, then publishes and consumes a message. Intended
            for use by monitoring tools.

        :param vhost: The vhost name to check
        :type vhost: str
        """
        return self._get(
            url=self.url + '/api/aliveness-test/{0}'.format(
                urllib.parse.quote_plus(vhost)
            ),
            headers=self.headers,
            auth=self.auth
        )
