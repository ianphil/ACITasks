#!/usr/bin/env python
import sys
import logging


class Logger:
    def __init__(self):
        self.level = logging.INFO
        self.format = "%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s"

        logging.basicConfig(
            level=self.level,
            format=self.format,
            handlers=[
                logging.FileHandler("acitask.log"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        self.logger = logging.getLogger()

    # Resource Group =====================================================
    def resource_group_creating(self, resource_group_name):
        self.logger.info(f"Creating resource group: {resource_group_name}")

    def resource_group_created(self, resource_group_name):
        self.logger.info(f"Created resource group {resource_group_name}")

    def resource_group_deleting(self, resource_group_name):
        self.logger.info(f"Deleting resource group: {resource_group_name}")

    def resource_group_deleted(self, resource_group_name):
        self.logger.info(f"Deleted resource group: {resource_group_name}")

    def resource_group_exist(self, resource_group_name):
        self.logger.info(f"Resouce group exists: {resource_group_name}")

    def resource_group_not_exist(self, resource_group_name):
        self.logger.info(f"Resource group does not exist: {resource_group_name}")

    # Container ===========================================================
    def container_description_creating(self, container_name):
        self.logger.info(f"Creating container description: {container_name}")

    def container_description_created(self, container_name):
        self.logger.info(f"Creatied container description: {container_name}")

    def container_command_executing(self, container_name):
        self.logger.info(f"Executing command for: {container_name}")

    def container_command_executed(self, container_name):
        self.logger.info(f"Executed command for {container_name}")

    # Container group =====================================================
    def container_group_creating(self, container_group_name):
        self.logger.info(f"Creating container group: {container_group_name}")

    def container_group_created(self, container_group_name):
        self.logger.info(f"Created container group: {container_group_name}")

    def container_group_deleting(self, container_group_name):
        self.logger.info(f"Deleting container group: {container_group_name}")

    def container_group_deleted(self, container_group_name):
        self.logger.info(f"Deleted container group: {container_group_name}")

    def container_group_exist(self, container_group_name):
        self.logger.info(f"Container group exists: {container_group_name}")

    def container_group_not_exist(self, container_group_name):
        self.logger.info(f"Container group does not exist: {container_group_name}")

    def container_group_starting(self, container_group_name):
        self.logger.info(f"Starting container group: {container_group_name}")

    def container_group_started(self, container_group_name):
        self.logger.info(f"Started container group: {container_group_name}")

    def container_group_stopping(self, container_group_name):
        self.logger.info(f"Stopping container group: {container_group_name}")

    def container_group_stopped(self, container_group_name):
        self.logger.info(f"Stopped container group: {container_group_name}")
