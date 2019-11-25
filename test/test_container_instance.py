#!/usr/bin/env python
from pytest import fixture
from aci_tasks.cloud import ContainerInstance
from aci_tasks.logger import Logger
from aci_tasks.config import Config, TaskType


@fixture
def strong_container_instance():
    return ContainerInstance(Logger(), Config(TaskType.STRONG))


@fixture
def weak_container_instance():
    return ContainerInstance(Logger(), Config(TaskType.WEAK))


def test_create_strong(strong_container_instance):
    container = strong_container_instance.create()
    assert container.image == strong_container_instance.config.container_image


def test_create_weak(weak_container_instance):
    container = weak_container_instance.create()
    assert container.image == weak_container_instance.config.container_image
