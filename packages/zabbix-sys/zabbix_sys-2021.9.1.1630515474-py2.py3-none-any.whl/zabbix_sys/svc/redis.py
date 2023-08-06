# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import redis
import re
import sys


class Redis:

    def __init__(self, cfg, logger):

        self.logger = logger
        self.dsn = []
        if not cfg:
            cfg = {}

        instances = cfg.get("redis", [])

        for instance in instances:
            dsn = {}
            dsn.update({"password": instance.get("password", None)})
            dsn.update({"host": instance.get("hostname", "127.0.0.1")})
            dsn.update({"port": instance.get("port", "6379")})
            dsn.update({"socket_timeout": 1})
            self.dsn.append(dsn)

        if not instances:
            self.dsn.append({
                "password": None,
                "hostname": "127.0.0.1",
                "port": "6379"
            })

    def lld(self):

        result = {"data": []}
        for dsn in self.dsn:
            try:
                cluster = False
                sentinel = False
                standalone = False
                cnx = redis.Redis(**dsn)
                res = cnx.execute_command("INFO")

                if res["redis_mode"] == "cluster":
                    cluster = True
                if res["redis_mode"] == "sentinel":
                    sentinel = True
                if res["redis_mode"] == "standalone":
                    standalone = True

                result["data"].append({
                    "cluster": cluster,
                    "sentinel": sentinel,
                    "standalone": standalone,
                    "hostname": dsn["host"],
                    "port": dsn["port"],
                    "version": res["redis_version"]
                })
            except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
                continue
            except Exception as err:
                self.logger.error(msg=err.__str__(), exc_info=False)
                sys.exit(1)

        return result

    def raw_info(self, hostname, port):

        result = {}

        for dsn in self.dsn:
            if dsn["host"] == str(hostname) and str(dsn["port"]) == str(port):
                try:
                    cnx = redis.Redis(**dsn)
                    res = cnx.execute_command("INFO")
                    for key, value in res.items():
                        result.update({str(key).lower(): value})

                except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
                    continue
                except Exception as err:
                    self.logger.error(msg=err.__str__(), exc_info=False)
                    sys.exit(1)

        return result

    def raw_cluster(self, hostname, port):

        result = {}

        for dsn in self.dsn:
            if dsn["host"] == str(hostname) and str(dsn["port"]) == str(port):
                try:
                    cnx = redis.Redis(**dsn)
                    res = cnx.execute_command("CLUSTER INFO")
                    for key, value in res.items():
                        result.update({str(key).lower(): str(value)})

                    res = cnx.execute_command("CLUSTER NODES")
                    status = {}
                    for key, value in res.items():
                        if "myself" in value["flags"]:
                            value["flags"] = str(value["flags"]).replace("myself", "").replace(",", "")
                            result.update({"cluster_role": value["flags"]})
                        status.update({
                            str(key): str(value["flags"])
                        })
                    result.update({
                        "nodes": status
                    })

                except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError, redis.exceptions.ResponseError):
                    continue
                except Exception as err:
                    self.logger.error(msg=err.__str__(), exc_info=False)
                    sys.exit(1)

        return result
