#!/usr/bin/env python
import time
from config import Config, TaskType
from logger import Logger
from cloud.aci_container import AciContainer
from cloud.aci_container_group import AciContainerGroup
from cloud.aci_resource_group import AciResourceGroup

if __name__ == "__main__":
    '''
    Note: The tests do these things also. From root of project
    just run "pytest"
    '''

    # Create Strong task container and exec command
    strong_config = Config(TaskType.STRONG)
    logger = Logger()

    rg = AciResourceGroup(logger, strong_config)
    rg.create()

    strong_container_group = AciContainerGroup(logger, strong_config)
    strong_container_group.create()

    strong_container = AciContainer(logger, strong_config)
    strong_container.execute_command('/strong_task/dog.py')

    # Create week task container and start/stop to exec command
    weak_config = Config(TaskType.WEAK)

    weak_container_group = AciContainerGroup(logger, weak_config)
    weak_container_group.create()

    weak_container_group.stop()

    time.sleep(60)

    weak_container_group.start()
    weak_container_group.stop()

    # Clean up
    rg.delete()
