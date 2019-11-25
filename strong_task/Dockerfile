FROM python:3.7-alpine3.9

RUN mkdir /strong_task
COPY strong_task/ /strong_task
RUN pip install -r /strong_task/requirements.txt \
    && chmod +x /strong_task/dog.py

CMD tail -f /dev/null