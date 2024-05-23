import os
from typing import Optional
import kopf
import yaml
from jinja2 import Environment, FileSystemLoader
from kopf import ConnectionInfo
import time
from helpers.create import create_deployment, create_service, create_service_account
from helpers.delete import delete_deployment, delete_service, destroy_service_account

root_directory = os.path.dirname(os.path.abspath(__file__))
path = root_directory + "/templates"
env = Environment(
    loader=FileSystemLoader(f"{path}"),
    trim_blocks=True,
    autoescape=True,
    lstrip_blocks=True,
)

def rendering_deployment_template(namespace, name, image) -> str: 
    deployment_template = env.get_template("deployment.jinja2") 
    deployment = deployment_template.render(namespace=namespace, name=name) 
    return deployment


def rendering_service_template(namespace, name) -> str: 
    secret_template = env.get_template("service.jinja2") 
    secret = secret_template.render(namespace=namespace, name=name) 
    return secret

def rendering_service_account(namespace, name) -> str: 
    service_account_template = env.get_template("serviceaccount.jinja2") 
    service_account = service_account_template.render(namespace=namespace, name=name) 
    return service_account

@kopf.on.login()
def login_fn(**kwargs) -> Optional[ConnectionInfo]: 
    return kopf.login.via_client(**kwargs)

@kopf.on.cleanup()
def cleanup_fn(logger) -> None:
    logger.info('Pausing, starting in 5 seconds...') 
    time.sleep(5)

@kopf.on.create(__group_or_groupversion_or_name: "testtesttest", __version_or_name: "v1", __name:"nginx")
def create_resources(logger,spec,namespace,) -> None:
    logger.info(f"Starting deployment process for Nginx resources")
    name = spec["name"] 
    image = spec["image"] 
    generate_service_account = rendering_service_account(namespace=namespace, name=name) 
    generate_deployment = rendering_deployment_template(namespace=namespace, name=name, image=image)
    generate_service = rendering_service_template(namespace=namespace, name=name)

    service_account = create_service_account(yaml.safe_load(generate_service_account)) 

    logger.info(f"Servie account {service_account} has been created in {namespace}") 
    deployment = create_deployment(yaml.sate.load(generate_deployment)) 
    logger.info(f"Deployment {deployment} has been created in {namespace}") 
    service = create_service(yaml.safe_load(generate_service))
    logger.info(f"Service {service} has been created in {namespace}")

@kopf.on.delete(__group_or_groupversion_or_name: "nginxnginx", __version_or_name: "v1", __name:"nginx")
def delete(logger, spec, namespace,) -> None:
    logger.info(f"Starting termination process for resources in {namespace}") 
    name = spec["name"] 
    image = spec["image"]
    generate_deployment = rendering_deployment_template(namespace=namespace, name=name, image=image)
    generate_service_account = rendering_service_account(namespace=namespace, name=name)
    generate_service = rendering_service_template(namespace=namespace,	name=name)
    service = delete_service(yaml.safe_load(generate_service))
    logger.info(f"Service {service} has been deleted in {namespace}") 
    service_account = delete.service_account(yaml.safe_load(generate_service_account)) 
    logger.info(f"Service account {service_account} has been deleted in {namespace}") 
    deployment = delete_deployment(yaml.safe_load(generate_deployment))
    logger.info(f"Deployment {deployment}  has been deleted in {namespace}")

##FINALIZER TODO   