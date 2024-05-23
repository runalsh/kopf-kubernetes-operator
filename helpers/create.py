import kubernetes
import pykube

api = kubernetes_api()

k8s_client = create_k8s_client().CustomObjectsApi()
core_api = create_k8s_client().CoreV1Api()

def create_service(template):
    kopf.adopt(template)
    service = pykube.Service(api, template)
    service.create()
    return service

def create_deployment(template):
    kopf.adopt(template)
    deployment = pykube.Deployment(api, template)
    deployment.create()
    return deployment

def create_service_account(template):
    kopf.adopt(template)
    service_account = pykube.ServiceAccount(api, template)
    service_account.create()
    return service_account