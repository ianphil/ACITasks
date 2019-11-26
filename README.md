# Azure Container Instances - Task-based workloads

Azure Container Instances (ACI) provides a platform for running containers without the management overhead of VMs, Docker, or Kubernetes. In this, it's very appealing for workloads that don't necessarily need a lot of orchestration. Task-based workloads are a great match for ACI. They are simple actions that need to be performed like moving files, notifying a queue, or posting a webhook. This repository is an opinionated way of using ACI to execute task-based workloads.

# Architecture

This creates two types of tasks. We'll explore what they are soon, but for now, each task creates it's own ACI group and contains a single container. The library found in `aci_tasks` folder contains the command and control code to create/execute the container group or containers. The code in the container simply posts a JSON body to a webhook.

![image](https://user-images.githubusercontent.com/17349002/69636966-b97c8000-1025-11ea-8f51-7931e6781dda.png)

# Task Types

Each task posts a message to a webhook. They are both container images hosted on Docker Hub so no authentication is required to download the images. The code for each container is at the root of the repo in their own folders.

 - __Strong Task__ - A strong task type expects the container to stay alive in ACI. Using the `execute_command` call (similar to `docker exec`) we run the strong.py script to post. The container should have a setting of restart always.

 - __Weak task__ - A week task is based on an on/off workload pattern. The ACI group can either be persistent or removed and recreated. If the group is persistent then the container instance in the group can be started and stopped. The startup command of this container calls the script, we then expect the container to 'die'.

 # Using the ACI_Task Command and Control Library

 This library expects Environmental Variables to be contained in a `.env` file. A `sample.env` file is provided with no values in the repo. Rename this file and configure the values. The library will parse and load these for you, so no fussing with xargs or the likes.

 After that, you can run the tests. These are integration tests and will create, execute, and destroy all the resources described above.

 There is an example use of the library also contained in `main.py`. This will do similar work to the tests, and is provided only for example use:

To execute `main.py`

0. Install Linux if you haven't already :-)
1. Create a virtualenv `python3 -m venv .venv`
2. Activate the virtualenv `. .venv/bin/activate`
3. Install the dependancies `pip install -r requirements.txt`
4. Run the file `python main.py`



*main.py Contents*


 ```python
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
 ```