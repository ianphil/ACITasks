# Strong Task Container

This container is a "strong task" based workload. Strong tasks workload keep the container running and execute commands in it. It is inteded to run a script:

 - python strong_task/dog.py

This simply posts to: [https://hookbin.com/](https://hookbin.com/).

## To use them locally follow these steps:

1. Build the container:

`docker build -t strong_task:01 strong_task/.`

2. Run the container:

`docker run -d --rm --name strong_task -e "ENDPOINTURL=https://hookb.in/mZz671L0bXCBVLpJXLkx" strong_task:01`

3. Execute commands in the container:

```bash
docker exec -it strong_task python /strong_task/dog.py
```

4. Remove the container:

`docker stop strong_task`