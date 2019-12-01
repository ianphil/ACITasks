#!/usr/bin/env python
import time
from aci_tasks.config import Config, TaskType
from aci_tasks.logger import Logger
from aci_tasks.cloud.aci_container import AciContainer
from aci_tasks.cloud.aci_container_group import AciContainerGroup
from aci_tasks.cloud.aci_resource_group import AciResourceGroup
from aci_tasks.cloud.aci_key_vault import AciKeyVaultManager, AciKeyVaultSecretStore


if __name__ == "__main__":
    """
    Note: The tests do these things also. From root of project
    just run "pytest"
    """

    # Create Strong task container and exec command
    strong_config = Config(TaskType.STRONG)
    logger = Logger()

    rg = AciResourceGroup(logger, strong_config)
    rg.create()

    # strong_container_group = AciContainerGroup(logger, strong_config)
    # strong_container_group.create()

    # strong_container = AciContainer(logger, strong_config)
    # strong_container.execute_command('/strong_task/dog.py')

    # # Create week task container and start/stop to exec command
    # weak_config = Config(TaskType.WEAK)

    # weak_container_group = AciContainerGroup(logger, weak_config)
    # weak_container_group.create()

    # weak_container_group.stop()

    # time.sleep(60)

    # weak_container_group.start()
    # weak_container_group.stop()

    # # Create Key Vault
    # key_vault_manager = AciKeyVaultManager(strong_config)
    # key_vault_manager.create()

    # time.sleep(60)

    # # Key Vault Store examples
    # # TODO: Need to write code to create Key Vault
    # config_store = AciKeyVaultSecretStore()

    # config_store["NAME"] = "Ian Philpot"
    # config_store["JOB"] = "engineer"

    # for k, v in config_store.items():
    #     print(f'Name: {k} \t\tValue: {v}')

    # Clean up
    rg.delete()
