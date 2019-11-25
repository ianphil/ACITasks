#!/usr/bin/env python
import os
from enum import Enum, auto


class TaskType(Enum):
    STRONG = auto()
    WEAK = auto()


class Config():
    def __init__(self, task_type: TaskType):
        if os.getenv('RESOURCEGROUPNAME') is None:
            _set_env_vars()

        self.resource_group_name = \
            os.getenv('RESOURCEGROUPNAME')

        self.resource_group_loation = \
            os.getenv('RESOURCEGROUPLOCATION')

        if task_type == TaskType.STRONG:
            self.container_group_name = \
                os.getenv('STRONGCONTAINERGROUPNAME')

            self.container_image = \
                os.getenv('STRONGCONTAINERIMAGENAME')

        if task_type == TaskType.WEAK:
            self.container_group_name = \
                os.getenv('WEAKCONTAINERGROUPNAME')

            self.container_image = \
                os.getenv('WEAKCONTAINERIMAGENAME')

        self.subscription_id = \
            os.getenv("SUBSCRIPTIONID")

        self.client_id = \
            os.getenv("AZURE_CLIENT_ID")

        self.client_secret = \
            os.getenv("AZURE_CLIENT_SECRET")

        self.tenant_id = \
            os.getenv("AZURE_TENANT_ID")

        self.endpoint_url = \
            os.getenv("ENDPOINTURL")


def _set_env_vars():
    current_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.abspath(os.path.join(current_path, os.pardir))

    with open(f'{file_path}/.env') as env_file:
        [_parse_set_env_var(l) for l in env_file.readlines()]


def _parse_set_env_var(line):
    data = line.strip('\n').split('=', 1)

    try:
        os.environ[data[0]] = str(data[1])
    except IndexError:
        pass
