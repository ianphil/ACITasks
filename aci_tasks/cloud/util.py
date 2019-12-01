#!/usr/bin/env python
import time
import websocket
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.containerinstance import ContainerInstanceManagementClient


def _poll_for_complete(result):
    while result.done() is False:
        time.sleep(1)


def _get_ci_client(config):
    return ContainerInstanceManagementClient(
        _get_credentials(config), config.subscription_id
    )


def _get_credentials(config) -> ServicePrincipalCredentials:
    return ServicePrincipalCredentials(
        client_id=config.client_id, secret=config.client_secret, tenant=config.tenant_id
    )


def _start_exec_pipe(web_socket_uri, password):
    ws = websocket.create_connection(web_socket_uri)
    try:
        ws.send(password)
    except websocket.WebSocketException:
        pass
