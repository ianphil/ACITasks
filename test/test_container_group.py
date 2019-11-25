#!/usr/bin/env python
import time
from pytest import fixture
from aci_tasks.cloud.aci_container import AciContainer
from aci_tasks.cloud.aci_container_group import AciContainerGroup
from aci_tasks.cloud.aci_resource_group import AciResourceGroup
from aci_tasks.logger import Logger
from aci_tasks.config import Config, TaskType


@fixture(scope="session", autouse=True)
def setup():
    rg = AciResourceGroup(Logger(), Config(TaskType.STRONG))
    rg.create()
    yield
    rg.delete()


@fixture
def strong_container_instance():
    return AciContainer(Logger(), Config(TaskType.STRONG))


@fixture
def strong_container_group():
    return AciContainerGroup(Logger(), Config(TaskType.STRONG))


@fixture
def weak_container_group():
    return AciContainerGroup(Logger(), Config(TaskType.WEAK))


def test_strong_create(strong_container_group):
    strong_container_group.create()
    assert strong_container_group._exists() is True


def test_strong_execute(strong_container_instance):
    '''This will post body=dog to https://hookbin.com/mZz671L0bXCBVLpJXLkx'''
    strong_container_instance.execute_command('/strong_task/dog.py')
    assert 1 == 1  # TODO: need to figureout how to assert this


def test_strong_delete(strong_container_group):
    strong_container_group.delete()
    assert strong_container_group._exists() is False


def test_weak_create(weak_container_group):
    '''This will post body=cat to https://hookbin.com/mZz671L0bXCBVLpJXLkx'''
    weak_container_group.create()
    assert weak_container_group._exists() is True


def test_weak_stop(weak_container_group):
    weak_container_group.stop()
    time.sleep(60)
    assert 1 == 1  # TODO: need to figureout how to assert this


def test_weak_start(weak_container_group):
    '''This will post body=cat to https://hookbin.com/mZz671L0bXCBVLpJXLkx'''
    weak_container_group.start()
    assert 1 == 1  # TODO: need to figureout how to assert this


def test_weak_delete(weak_container_group):
    weak_container_group.delete()
    assert weak_container_group._exists() is False


# To verify tests there should be a dog and two cats posted to:
# https://hookbin.com/mZz671L0bXCBVLpJXLkx
