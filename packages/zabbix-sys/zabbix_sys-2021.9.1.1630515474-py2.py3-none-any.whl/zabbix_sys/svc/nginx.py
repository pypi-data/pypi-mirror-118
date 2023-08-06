
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import re
import requests
import requests.auth
import requests.exceptions
import sys


class Nginx:

    def __init__(self, cfg, logger):

        self.logger = logger
        self.dsn = {}
        if not cfg:
            cfg = {}

        self.dsn.update({"username": cfg.get('nginx', {}).get('username', "")})
        self.dsn.update({"password": cfg.get('nginx', {}).get('password', "")})
        self.dsn.update({"scheme": cfg.get('nginx', {}).get('scheme', "http")})
        self.dsn.update({"hostname": cfg.get('nginx', {}).get('hostname', "127.0.0.1")})
        self.dsn.update({"port": cfg.get('nginx', {}).get('port', "8080")})
        self.dsn.update({"url": cfg.get('nginx', {}).get('url', "/status")})
        self.dsn.update({"timeout": 2})

        self.url = ""
        self.url += str(self.dsn['scheme']) + "://"
        self.url += str(self.dsn['hostname']) + ":" + str(self.dsn['port'])
        self.url += self.dsn["url"]

        if self.dsn['username'] and self.dsn['password']:
            self.auth = requests.auth.HTTPBasicAuth(username=self.dsn['username'], password=self.dsn['password'])
        else:
            self.auth = None

    @property
    def __get__status__(self):
        try:
            if self.auth:
                response = requests.get(url=self.url, auth=self.auth)
            else:
                response = requests.get(self.url)

            if response.status_code == 200 and "Active connections:" in response.text:
                return response.text
            else:
                return None
        except Exception:
            raise

    def lld_status(self):

        result = {
            'data': []
        }

        try:
            response = self.__get__status__
            if response:
                result['data'].append(
                    {"_": "", "stats": True}
                )
            return result

        except requests.exceptions.ConnectionError:
            return result

        except Exception as err:
            self.logger.error(msg=err.__str__(), exc_info=False)
            sys.exit(1)

    def raw_status(self):

        result = {}
        try:
            response = self.__get__status__
            if response:
                result.update(
                    {
                        'active': re.search('^Active connections:\s(\d+)', response).group(1),
                        'accepts': re.search('\s+(\d+)\s+(\d+)\s+(\d+)', response).group(1),
                        'handled': re.search('\s+(\d+)\s+(\d+)\s+(\d+)', response).group(2),
                        'requests': re.search('\s+(\d+)\s+(\d+)\s+(\d+)', response).group(3),
                        'reading': re.search('Reading:\s+(\d+)', response).group(1),
                        'writing': re.search('Writing:\s+(\d+)', response).group(1),
                        'waiting': re.search('Waiting:\s+(\d+)', response).group(1)
                    }
                )
            return result

        except requests.exceptions.ConnectionError:
            return result

        except Exception as err:
            self.logger.error(msg=err, exc_info=False)
            sys.exit(1)
