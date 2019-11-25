#!/usr/bin/env python
import sys
import logging


class Logger():
    def __init__(self):
        self.level = logging.INFO
        self.format = \
            "%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s"

        logging.basicConfig(
            level=self.level, format=self.format, handlers=[
                logging.FileHandler("acitask.log"),
                logging.StreamHandler(sys.stdout)
            ])

        self.logger = logging.getLogger()

    def resource_group_created(self):
        self.logger.info("Resource group created")

    def resource_group_deleted(self):
        self.logger.info("Resource group deleted")

    def resource_group_exist(self):
        self.logger.info("Resouce group exists")

    def resource_group_not_exist(self):
        self.logger.info("Resource group does not exist")

    def container_created(self):
        self.logger.info("Container instance created")

    def container_group_created(self):
        self.logger.info("Container group created")

    def container_group_deleted(self):
        self.logger.info("Container group deleted")

    def container_group_exist(self):
        self.logger.info("Container group exists")

    def container_group_not_exist(self):
        self.logger.info("Container group does not exist")
