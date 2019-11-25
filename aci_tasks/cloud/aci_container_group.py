#!/usr/bin/env python
from aci_tasks.cloud.util import _get_ci_client, _poll_for_complete
from aci_tasks.cloud.aci_container import AciContainer
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.containerinstance.models import (
    ContainerGroup,
    OperatingSystemTypes,
    ContainerGroupRestartPolicy,
    ContainerGroupIdentity,
    ResourceIdentityType
)


class AciContainerGroup():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def create(self):
        if self._exists():
            return

        ci_client = _get_ci_client(self.config)
        ci = AciContainer(self.logger, self.config)
        container = ci.create()

        group = ContainerGroup(
            location=self.config.resource_group_loation,
            containers=[container],
            os_type=OperatingSystemTypes.linux,
            restart_policy=ContainerGroupRestartPolicy.never,
            identity=ContainerGroupIdentity(
                type=ResourceIdentityType.system_assigned
            ))

        try:
            result = ci_client.container_groups.create_or_update(
                self.config.resource_group_name,
                self.config.container_group_name,
                group)

            _poll_for_complete(result)
        except CloudError as ce:
            if ce.inner_exception.error == "InaccessibleImage":
                self.logger.logger.warning("Did you forget to push the image?")

        self.logger.container_group_created()

    def delete(self):
        if not self._exists():
            return

        ci_client = _get_ci_client(self.config)

        try:
            ci_client.container_groups.delete(
                self.config.resource_group_name,
                self.config.container_group_name)
        except CloudError as ce:
            self.logger.logger.warning(
                f'Delete Container Group Error: {ce.message}')

        self.logger.container_group_deleted()

    def start(self):
        if not self._exists():
            return

        ci_client = _get_ci_client(self.config)

        try:
            result = ci_client.container_groups.start(
                self.config.resource_group_name,
                self.config.container_group_name
            )

            _poll_for_complete(result)
        except CloudError:
            pass

    def stop(self):
        if not self._exists():
            return

        ci_client = _get_ci_client(self.config)

        try:
            ci_client.container_groups.stop(
                self.config.resource_group_name,
                self.config.container_group_name
            )
        except CloudError:
            pass

    def _exists(self) -> bool:
        ci_client = _get_ci_client(self.config)

        try:
            c = ci_client.container_groups.get(
                self.config.resource_group_name,
                self.config.container_group_name
            )

            if c.containers[0].image != self.config.container_image:
                return False

            self.logger.container_group_exist()
            return True
        except CloudError as ce:
            if ce.inner_exception.error == "ResourceGroupNotFound":
                self.logger.logger.warning(
                    "You need to create a resource group")
            if ce.inner_exception.error == "ResourceNotFound":
                self.logger.container_group_not_exist()
                return False
