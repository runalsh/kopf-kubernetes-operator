import os
from typing import Optional
import kopf
import yaml
from jinja2 import Environment, FileSystemLoader
from kopf import ConnectionInfo
import time
from helpers.create import create_deployment, create_service, create_
from helpers.delete import delete_deployment, delete_service, delete_

root_directory = os.path.dirname(os.path.abspath(__file__))
path = root_directory + "/templates"
env = Environment(
    loader=FileSystemLoader(f"{path}"),
    trim_blocks=True,
    autoescape=True,
    lstrip_blocks=True,
)









