# -*- coding=utf-8 -*-
import nacos
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from nacos import DEFAULT_GROUP_NAME

logging.basicConfig()
logger = logging.getLogger(__name__)

class NacosAutoClient:

    def __init__(self, server_addresses, namespace, service_name, ip, port, cluster_name=None,
                 group_name=DEFAULT_GROUP_NAME):
        self.sched = BackgroundScheduler()
        self.server_addresses = server_addresses
        self.namespace = namespace
        params = {
            "ip": ip,
            "port": port,
            "serviceName": service_name,
            "clusterName": cluster_name,
            "groupName": group_name
        }
        self.params = params
        self.client = nacos.NacosClient(server_addresses, namespace=namespace)

    def start(self):
        if self.client.add_naming_instance(self.params["serviceName"], self.params["ip"], self.params["port"],
                                           cluster_name=self.params["clusterName"],
                                           group_name=self.params["groupName"]):
            self.sched.add_job(self.send_beat, 'interval', seconds=5)
            self.sched.start()
        else:
            logger.info("add naming instance failure")

    def send_beat(self):
        self.client.send_heartbeat(self.params["serviceName"], self.params["ip"], self.params["port"],
                                   cluster_name=self.params["clusterName"],
                                   group_name=self.params["groupName"])
        logger.info("[send_beat] serviceName:%s  ip:%s port:%s send beat" % (
        self.params["serviceName"], self.params["ip"], self.params["port"]))

    def shutdown(self):
        self.sched.shutdown()
