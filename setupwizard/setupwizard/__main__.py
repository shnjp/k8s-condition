import os

import kubernetes
from sanic import Sanic, response


if os.environ.get('K8S_CONDITION_IN_LOCAL') == '1':
    kubernetes.config.load_kube_config()
    CLUSTER_NAMESPACE = 'k8s-condition'
else:
    kubernetes.config.load_incluster_config()
    CLUSTER_NAMESPACE = open('/var/run/secrets/kubernetes.io/serviceaccount/namespace').read().strip()
    print(f'initilized at cluster @ {CLUSTER_NAMESPACE}')


kapi_apps = kubernetes.client.AppsV1Api()
kapi_core = kubernetes.client.CoreV1Api()

app = Sanic(name="setupwizard")


@app.route("/")
async def test(request):
    return response.html(
        '''\
<div style="background: red;">hello setupwizard 2</div>
<div>
    <a href="/go-main">Launch Main App</a>
</div>
'''
    )


@app.route('/go-main')
async def go_main(request):
    """replicaの数を調整して、本番とセットアップウィザードを切り替える"""
    print('patch mainapp')
    # body = [{"op": "replace", "path": "spec.replicas", "value": 1}]
    body = {'spec': {'replicas': 1}}
    ret = kapi_apps.patch_namespaced_deployment('mainapp', CLUSTER_NAMESPACE, body=body)
    print('mainapp', ret)

    print('patch service')
    body = {'spec': {'selector': {'app': 'mainapp'}}}
    ret = kapi_core.patch_namespaced_service('condition-test', CLUSTER_NAMESPACE, body=body)
    print('service', ret)

    print('patch setupwizard')
    body = {'spec': {'replicas': 0}}
    ret = kapi_apps.patch_namespaced_deployment('setupwizard', CLUSTER_NAMESPACE, body=body)
    print('setupwizard', ret)

    return response.html(
        '''\
<head>
<meta http-equiv="refresh" content="10;URL=/">
</head>
10秒後に <a href="/">/</a> をリロードするぜ
'''
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
