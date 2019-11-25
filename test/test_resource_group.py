#!/usr/bin/env python
from pytest import fixture
from aci_tasks.cloud.aci_resource_group import AciResourceGroup
from aci_tasks.logger import Logger
from aci_tasks.config import Config, TaskType


@fixture
def resource_group():
    return AciResourceGroup(Logger(), Config(TaskType.WEAK))


def test_create(resource_group):
    resource_group.create()
    assert resource_group._exists() is True


def test_delete(resource_group):
    resource_group.delete()
    assert resource_group._exists() is False
