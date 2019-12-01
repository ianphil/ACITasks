#!/usr/bin/env python
from aci_tasks.cloud.util import _get_ci_client, _start_exec_pipe
from azure.mgmt.containerinstance.models import (
    Container,
    ResourceRequests,
    ResourceRequirements,
    EnvironmentVariable,
    ContainerExecResponse,
    ContainerExecRequestTerminalSize
)


class AciContainer():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def create(self):
        self.logger.container_creating(self.config.container_group_name)

        endpoint_env = EnvironmentVariable(
            name="ENDPOINTURL", value=self.config.endpoint_url)
        container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
        container_resource_requirements = ResourceRequirements(
            requests=container_resource_requests)

        self.logger.container_created(self.config.container_group_name)

        return Container(name=self.config.container_group_name,
                         image=self.config.container_image,
                         resources=container_resource_requirements,
                         environment_variables=[endpoint_env])

    def execute_command(self, command):
        self.logger.container_command_executing(
            self.config.container_group_name)

        ci_client = _get_ci_client(self.config)
        res: ContainerExecResponse = ci_client.container.execute_command(
            resource_group_name=self.config.resource_group_name,
            container_group_name=self.config.container_group_name,
            container_name=self.config.container_group_name,
            command=command,
            terminal_size=ContainerExecRequestTerminalSize(rows=600, cols=800))

        _start_exec_pipe(res.web_socket_uri, res.password)

        self.logger.container_command_executed(
            self.config.container_group_name)
