#!/usr/bin/env python

import os
import requests

ENDPOINT = os.getenv("ENDPOINTURL")
name = "Weak"
data = {'NAME': name}
r = requests.post(url=ENDPOINT, json=data)

print(f'Status code:\t{r.status_code}\nText:\t\t{r.text}')
