# Weak Task Container

This container is a "Weak task" based workload. Weak tasks workload do not keep the container running and executes a command on startup. It is inteded to run a script:

 - python weak_task/cat.py

This simply posts to: [https://hookbin.com/](https://hookbin.com/).

## To use them locally follow these steps:

1. Build the container:

`docker build -t weak_task:01 weak_task/.`

2. Run the container:

`docker run -it --rm --name weak_task -e "ENDPOINTURL=https://hookb.in/mZz671L0bXCBVLpJXLkx" weak_task:01`
