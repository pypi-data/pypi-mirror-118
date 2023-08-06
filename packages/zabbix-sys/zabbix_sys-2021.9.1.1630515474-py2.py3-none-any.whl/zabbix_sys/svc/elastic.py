
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import elasticsearch
import sys


class Elasticsearch:

    def __init__(self, cfg, logger):

        self.logger = logger
        self.dsn = {}
        if not cfg:
            cfg = {}

        self.dsn.update({"scheme": cfg.get("elasticsearch", {}).get("scheme", "http")})
        self.dsn.update({"hostname": cfg.get("elasticsearch", {}).get("hostname", "127.0.0.1")})
        self.dsn.update({"port": cfg.get("elasticsearch", {}).get("port", "9200")})

    def lld(self):

        result = {"data": []}

        try:

            cnx = elasticsearch.Elasticsearch(
                hosts=["{}://{}:{}".format(self.dsn["scheme"], self.dsn["hostname"], self.dsn["port"])]
            )

            nodes = cnx.nodes.info(node_id="_local")["nodes"]

            for key, value in nodes.items():
                result["data"].append({
                    "_": "",
                    "cluster": value.get("settings", {}).get("cluster", {}).get("name", ""),
                    "node": value.get("name", ""),
                    "node_id": key,
                    "version": value.get("version", "")
                })

        except elasticsearch.exceptions.ConnectionError:
            return result

        except Exception as ex:
            self.logger.error("Exception: {0}".format(ex.__str__()), exc_info=True)
            sys.exit(1)

        return result

    def status(self):

        result = {}

        try:
            cnx = elasticsearch.Elasticsearch(
                hosts=["{}://{}:{}".format(self.dsn["scheme"], self.dsn["hostname"], self.dsn["port"])]
            )

            nodes = cnx.nodes.info(node_id="_local")["nodes"]

            for key, value in nodes.items():

                result.update({
                    "_node_id": key,
                    "stats": cnx.nodes.stats(node_id=key)["nodes"][key],
                    "cluster": {
                        "stats": cnx.cluster.stats(),
                        "health": cnx.cluster.health()
                    }
                })

        except Exception as ex:
            self.logger.error("", ex)
            sys.exit(1)

        return result
