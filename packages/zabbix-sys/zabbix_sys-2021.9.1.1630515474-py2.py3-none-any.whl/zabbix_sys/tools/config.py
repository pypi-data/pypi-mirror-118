# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from zabbix_sys.tools.logger import get_logger
import os
import yaml
import platform
import pathlib
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger


CONFIGS = {
    'linux': [
        os.path.abspath(os.path.expanduser("~/.zabbix/config.yml")),
        os.path.abspath("/var/lib/zabbix/config.yml"),
        os.path.abspath("/etc/zabbix/config.yml")
    ],
    'darwin': [
        os.path.abspath(os.path.expanduser("~/.zabbix/config.yml")),
        os.path.abspath("/var/lib/zabbix/config.yml"),
        os.path.abspath("/etc/zabbix/config.yml")
    ],
    'windows': [
        os.path.abspath(os.path.expanduser("~\\.zabbix\\config.yml")),
        os.path.abspath("C:\\ProgramData\\Tools\\Zabbix\\config.yml")
    ]
}


class ConfigPlatformException(Exception):
    pass

class _ConfigElasticsearch(object):
    def __init__(self, config):
        self.hostname = config.get('hostname', '127.0.0.1')
        self.port = config.get('port', '9200')
        self.scheme = config.get('scheme', 'http')
        self.username = config.get('username', None)
        self.password = config.get('password', None)


class _ConfigMySQL(object):
    def __init__(self, config):

        if pathlib.Path('~/.my.cnf').expanduser().absolute().is_file():
            self.read_default_file = pathlib.Path('~/.my.cnf').expanduser().absolute().__str__()

        self.username = config.get('username', 'zabbix')
        self.password = config.get('password', 'zabbix')
        self.hostname = config.get('hostname', '127.0.0.1')
        self.port = config.get('port', '3306')


class _ConfigNginx(object):
    def __init__(self, config):
        self.hostname = config.get('hostname', '127.0.0.1')
        self.port = config.get('port', '8080')
        self.path = config.get('path', '/status')
        self.username = config.get('username', None)
        self.password = config.get('password', None)


class _ConfigRabbitMQ(object):
    def __init__(self, config):
        self.hostname = config.get('hostname', '127.0.0.1')
        self.port = config.get('port', '15672')
        self.username = config.get('username', 'zabbix')
        self.password = config.get('password', 'zabbix')
        self.scheme = config.get('scheme', 'http')



class Config():

    @staticmethod
    def __get_logger__():

        logging.captureWarnings(capture=True)
        logger = logging.getLogger()

        for handler in logger.handlers:
            logger.removeHandler(handler)

        log_file = 'zabbix_sys.log'

        if pathlib.Path('/var/log/zabbix').is_dir():
            try:
                with open('/var/log/zabbix/zabbix_sys.log', 'a'):
                    log_file = '/var/log/zabbix/zabbix_sys.log'
            except Exception:
                # Use current location (./) for log file
                pass

        logger_handler = logging.handlers.RotatingFileHandler(
            filename=log_file, mode='a', maxBytes=10 * 1024 * 1024, backupCount=5
        )
        logger_handler.setLevel(logging.ERROR)
        logger_handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
        logger.addHandler(logger_handler)
        return logger

    @staticmethod
    def __get_platform__():

        result = str(platform.system()).lower()

        if result not in ['linux', 'darwin', 'windows']:
            raise ConfigPlatformException("Platform unsupported")

        return result

    def __get_config_file__(self):

        config = {}
        config_files = []

        if str(platform.system()).lower() in ['linux', 'darwin']:
            config_files = [
                pathlib.Path("~/.zabbix/config.yml").expanduser().absolute(),
                pathlib.Path("/var/lib/zabbix/config.yml").absolute(),
                pathlib.Path("/etc/zabbix/config.yml").absolute()
            ]
        if str(platform.system()).lower() in ['windows']:
            config_files = [
                pathlib.Path("~\\.zabbix\\config.yml").expanduser().absolute(),
                pathlib.Path("{0}\\Tools\\Zabbix\\config.yml".format(os.getenv("PROGRAMDATA"))).absolute()
            ]

        for config_file in config_files:
            if pathlib.Path(config_file).is_file():
                try:
                    with open(config_file) as stream:
                        config = yaml.safe_load(stream=stream)
                        break
                except yaml.MarkedYAMLError as err:
                    self.logger.critical(
                        msg="Error when parse yaml config " + str(err.context_mark).strip(),
                        exc_info=False
                    )
                    raise

        return config

    def __init__(self):

        self.logger = self.__get_logger__()
        self.platform = self.__get_platform__()

        config = self.__get_config_file__()

        self.elasticsearch = _ConfigElasticsearch(config.get('elasticsearch', {}))
        self.mysql = _ConfigMySQL(config.get('mysql', {}))
        self.nginx = _ConfigNginx(config.get('nginx', {}))
        self.rabbitmq = _ConfigRabbitMQ(config.get('rabbitmq', {}))

def get_platform():

    system = str(platform.system()).lower()

    if system in CONFIGS.keys():
        return system
    else:
        return None


def get_config():

    system = get_platform()
    logger = get_logger()
    config = None

    if system:
        for f in CONFIGS[system]:
            if os.path.isfile(f):
                try:
                    with open(f) as stream:
                        config = yaml.safe_load(stream)
                    break
                except yaml.MarkedYAMLError as err:
                    logger.critical(msg="Error when parse yaml config " + str(err.context_mark).strip(), exc_info=False)
                    raise
    return config
