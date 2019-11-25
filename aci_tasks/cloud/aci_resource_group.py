#!/usr/bin/env python
from aci_tasks.cloud.util import _poll_for_complete, _get_credentials
from azure.mgmt.resource import ResourceManagementClient


class AciResourceGroup():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def create(self):
        if self._exists():
            return

        rg_client = self._get_rg_client()

        rg_client.resource_groups.create_or_update(
            self.config.resource_group_name,
            {"location": self.config.resource_group_loation})

        self.logger.resource_group_created()

    def delete(self):
        if not self._exists():
            return

        rg_client = self._get_rg_client()

        result = rg_client.resource_groups.delete(
            self.config.resource_group_name)

        _poll_for_complete(result)

        self.logger.resource_group_deleted()

    def _exists(self) -> bool:
        rg_client = self._get_rg_client()
        exists = rg_client.resource_groups.check_existence(
            self.config.resource_group_name)

        if exists:
            self.logger.resource_group_exist()
        else:
            self.logger.resource_group_not_exist()

        return exists

    def _get_rg_client(self) -> ResourceManagementClient:
        return ResourceManagementClient(
            _get_credentials(self.config), self.config.subscription_id)
