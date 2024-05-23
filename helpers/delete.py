
import kubernetes
import pykube

api = kubernetes_api()

k8s_client = create_k8s_client().CustomObjectsApi()
core_api = create_k8s_client().CoreV1Api()


def destroy_service(template):
    kopf.adopt(template)
    service = pykube.Service(api, template)
    service.delete()
    return service


def destroy_deployment(template):
    kopf.adopt(template)
    deployment = pykube.Deployment(api, template)
    deployment.delete()
    return deployment

def destroy_service_account(template):
    kopf.adopt(template)
    service_account = pykube.ServiceAccount(api, template)
    service_account.delete()
    return service_account