# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys
from pyrabbit2.api import Client
from pyrabbit2.http import NetworkError


class RabbitMQ:

    def __init__(self, cfg, logger):

        self.logger = logger
        self.dsn = {}
        if not cfg:
            cfg = {}

        self.dsn.update({"user": cfg.get('rabbitmq', {}).get('username', "guest")})
        self.dsn.update({"passwd": cfg.get('rabbitmq', {}).get('password', "guest")})
        self.dsn.update({"scheme": cfg.get('rabbitmq', {}).get('scheme', "http")})
        self.dsn.update({"hostname": cfg.get('rabbitmq', {}).get('hostname', "127.0.0.1")})
        self.dsn.update({"port": cfg.get('rabbitmq', {}).get('port', "15672")})

        self.dsn.update({
            'api_url': str(self.dsn['hostname']) + ":" + str(self.dsn['port'])
        })

        del self.dsn['hostname']
        del self.dsn['port']

        self.cnx = Client(**self.dsn)

    def lld_exchanges(self):

        result = {"data": []}

        try:
            self.cnx.is_alive()
            exchanges = self.cnx.get_exchanges()
            for exchange in exchanges:
                if exchange['name']:
                    result["data"].append({
                        'vhost': exchange['vhost'],
                        'name': exchange['name'],
                        'type': exchange['type'],
                        'internal': exchange['internal']
                    })
            return result
        except NetworkError:
            return result

        except Exception as err:
            self.logger.error(err.__str__(), exc_info=False)
            sys.exit(1)

    def lld_queues(self):

        result = {"data": []}

        try:
            self.cnx.is_alive()
            queues = self.cnx.get_queues()
            for queue in queues:
                if queue['name'] == 'aliveness-test':
                    continue
                delayed = False
                if "arguments" in queue and "x-dead-letter-exchange" in queue["arguments"]:
                    delayed = True
                result['data'].append({
                    'vhost': queue['vhost'],
                    'name': queue['name'],
                    'delayed': delayed
                })

            return result

        except NetworkError:
            return result

        except Exception as err:
            self.logger.error(err.__str__(), exc_info=False)
            sys.exit(1)

    def lld_server(self):

        result = {"data": []}

        try:
            self.cnx.is_alive()
            stats = self.cnx.get_overview()
            result["data"].append({
                "_": "",
                "rabbitmq_version": stats["rabbitmq_version"]
            })
            return result

        except NetworkError:
            return result

        except Exception as err:
            self.logger.error(err.__str__(), exc_info=False)
            sys.exit(1)

    def lld_shovels(self):

        result = {"data": []}

        try:
            self.cnx.is_alive()
            shovels = self.cnx.get_all_shovels()
            for shovel in shovels:
                result["data"].append({
                    'vhost': shovel['vhost'],
                    'name': shovel['name']
                })
            return result

        except NetworkError:
            return result

        except Exception as err:
            self.logger.error(err.__str__(), exc_info=False)
            sys.exit(1)

    def raw_exchanges(self, vhost, exchange_name):
        try:
            self.cnx.is_alive()
            result = self.cnx.get_exchange(vhost=vhost, name=exchange_name)
            return result
        except Exception as err:
            self.logger.error(msg=err.__str__(), exc_info=False)
            sys.exit(1)

    def raw_queues(self, vhost, queue):

        try:
            self.cnx.is_alive()
            result = self.cnx.get_queue(vhost=vhost, name=queue)
            if 'consumer_details' in result:
                del result['consumer_details']
            return result

        except Exception as err:
            self.logger.error(msg=err.__str__(), exc_info=False)
            sys.exit(1)

    def raw_server(self):

        try:
            self.cnx.is_alive()
            result = self.cnx.get_overview()

            hostname = ""
            for context in result['contexts']:
                if 'node' in context:
                    hostname = context['node']
                    break

            nodes = self.cnx.get_nodes()
            for node in nodes:
                if 'name' in node and node['name'] == hostname:
                    result.update({"node_stats": node})
            return result

        except Exception as err:
            self.logger.error(msg=err.__str__(), exc_info=False)
            sys.exit(1)

    def raw_shovels(self, vhost, shovel_name):

        try:
            self.cnx.is_alive()
            result = self.cnx.get_shovel(vhost=vhost, shovel_name=shovel_name)
            return result
        except Exception as err:
            self.logger.error(msg=err.__str__(), exc_info=False)
            sys.exit(1)
