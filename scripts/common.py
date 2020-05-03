from plano import *

def run_test():
    call("kubectl apply -f resources")

    namespaces = [
        "console",
        "store-1",
        "store-2",
        "store-3",
        "factory-1",
        "factory-2",
        "factory-3",
        "infra-1",
        "infra-2",
        "infra-3",
    ]

    for namespace in namespaces:
        if namespace.startswith("infra"):
            call(f"skupper -n {namespace} init --enable-proxy-controller=false")
        else:
            call(f"skupper -n {namespace} init --edge")

    with temp_working_dir():
        call("skupper -n infra-1 connection-token infra-1-token.yaml")
        call("skupper -n store-1 connect infra-1-token.yaml")
        call("skupper -n factory-1 connect infra-1-token.yaml")

        call("skupper -n infra-2 connection-token infra-2-token.yaml")
        call("skupper -n store-2 connect infra-2-token.yaml")
        call("skupper -n factory-2 connect infra-2-token.yaml")

        call("skupper -n infra-3 connection-token infra-3-token.yaml")
        call("skupper -n store-3 connect infra-3-token.yaml")
        call("skupper -n factory-3 connect infra-3-token.yaml")

        call("skupper -n infra-1 connect infra-2-token.yaml")
        call("skupper -n infra-2 connect infra-3-token.yaml")
        call("skupper -n infra-3 connect infra-1-token.yaml")

        call("skupper -n console connect infra-1-token.yaml")

    call("skupper -n infra-1 service create store-all 8080 --mapping http --aggregate json")
    call("skupper -n infra-1 service create factory-all 8080 --mapping http --aggregate json")
    call("skupper -n infra-1 service create factory-any 8080 --mapping http")

    for namespace in namespaces:
        if namespace.startswith("store"):
            call(f"skupper -n {namespace} expose deployment store --port 8080 --protocol http --address {namespace}") # A particular store
            call(f"skupper -n {namespace} bind store-all deployment store --protocol http") # All stores (multicast query)

        if namespace.startswith("factory"):
            call(f"skupper -n {namespace} expose deployment factory --port 8080 --protocol http --address {namespace}") # A particular factory
            call(f"skupper -n {namespace} bind factory-any deployment factory --protocol http") # Any factory (anycast)
            call(f"skupper -n {namespace} bind factory-all deployment factory --protocol http") # All factories (multicast query)

    call("kubectl -n console expose deployment console --port 9090 --target-port 8080 --type LoadBalancer")

def check_environment():
    call("kubectl version --client --short")
    call("skupper --version")
    call("curl --version")

# Eventually Kubernetes will make this nicer:
# https://github.com/kubernetes/kubernetes/pull/87399
# https://github.com/kubernetes/kubernetes/issues/80828
# https://github.com/kubernetes/kubernetes/issues/83094
def wait_for_resource(group, name):
    notice(f"Waiting for {group}/{name} to be available")

    for i in range(180):
        sleep(1)

        if call_for_exit_code(f"kubectl get {group}/{name}") == 0:
            break
    else:
        fail(f"Timed out waiting for {group}/{name}")

    if group == "deployment":
        try:
            call(f"kubectl wait --for condition=available --timeout 180s {group}/{name}")
        except:
            call(f"kubectl logs {group}/{name}")
            raise

def wait_for_connection(name):
    try:
        call(f"skupper check-connection --wait 180 {name}")
    except:
        call("kubectl logs deployment/skupper-router")
        raise

def get_ingress_ip(group, name):
    wait_for_resource(group, name)

    for i in range(180):
        sleep(1)

        if call_for_stdout(f"kubectl get {group}/{name} -o jsonpath='{{.status.loadBalancer.ingress}}'") != "":
            break
    else:
        fail(f"Timed out waiting for ingress for {group}/{name}")

    return call_for_stdout(f"kubectl get {group}/{name} -o jsonpath='{{.status.loadBalancer.ingress[0].ip}}'")
