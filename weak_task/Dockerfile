FROM python:3.7-alpine3.9

RUN mkdir /weak_task
COPY weak_task/ /weak_task
RUN pip install -r /weak_task/requirements.txt

CMD python /weak_task/cat.py