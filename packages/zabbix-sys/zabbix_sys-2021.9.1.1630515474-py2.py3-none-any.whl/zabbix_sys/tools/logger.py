# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import logging
import logging.handlers
import pathlib
from pythonjsonlogger import jsonlogger


def get_logger():

    logging.captureWarnings(capture=True)
    logger = logging.getLogger()

    for handler in logger.handlers:
        logger.removeHandler(handler)

    log_file = 'zabbix_sys.log'

    if pathlib.Path('/var/log/zabbix').is_dir():
        try:
            with open('/var/log/zabbix/zabbix_sys.log', 'a'):
                log_file = '/var/log/zabbix/zabbix_sys.log'
        except Exception as ex:
            # Use current location (./) for log file
            pass

    logger_handler = logging.handlers.RotatingFileHandler(
        filename=log_file, mode='a', maxBytes=10 * 1024 * 1024, backupCount=5
    )
    logger_handler.setLevel(logging.ERROR)
    logger_handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
    logger.addHandler(logger_handler)

    return logger
