#!/usr/bin/env python
import time
import websocket
from msrestazure.azure_exceptions import CloudError
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    Container,
    ResourceRequests,
    ResourceRequirements,
    EnvironmentVariable,
    ContainerGroup,
    OperatingSystemTypes,
    ContainerGroupRestartPolicy,
    ContainerExecResponse,
    ContainerExecRequestTerminalSize,
    ContainerGroupIdentity,
    ResourceIdentityType
)


class ResourceGroup():
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


class ContainerInstance():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def create(self):
        endpoint_env = EnvironmentVariable(
            name="ENDPOINTURL", value=self.config.endpoint_url)
        container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
        container_resource_requirements = ResourceRequirements(
            requests=container_resource_requests)

        self.logger.container_created()

        return Container(name=self.config.container_group_name,
                         image=self.config.container_image,
                         resources=container_resource_requirements,
                         environment_variables=[endpoint_env])

    def execute_command(self, command):
        ci_client = _get_ci_client(self.config)
        res: ContainerExecResponse = ci_client.container.execute_command(
            resource_group_name=self.config.resource_group_name,
            container_group_name=self.config.container_group_name,
            container_name=self.config.container_group_name,
            command=command,
            terminal_size=ContainerExecRequestTerminalSize(rows=600, cols=800))

        _start_exec_pipe(res.web_socket_uri, res.password)


class ContainerGroupInstance():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def create(self):
        if self._exists():
            return

        ci_client = _get_ci_client(self.config)
        ci = ContainerInstance(self.logger, self.config)
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


def _poll_for_complete(result):
    while result.done() is False:
        time.sleep(1)


def _get_ci_client(config):
    return ContainerInstanceManagementClient(
        _get_credentials(config), config.subscription_id
    )


def _get_credentials(config) -> ServicePrincipalCredentials:
    return ServicePrincipalCredentials(
        client_id=config.client_id,
        secret=config.client_secret,
        tenant=config.tenant_id
    )


def _start_exec_pipe(web_socket_uri, password):
    ws = websocket.create_connection(web_socket_uri)
    try:
        ws.send(password)
    except websocket.WebSocketException:
        pass
