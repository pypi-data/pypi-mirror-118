#!/bin/bash -x

function patchfunc {
MASTERS=$(oc get node --no-headers | wc -l)
[ "$MASTERS" == "3" ] || return 1
VROUTERS=$(oc wait -n tf --for condition=ready pod -l vrouter=vrouter1 | wc -l)
[ "$VROUTERS" == "3" ] || return 1
HOST_IP=$(oc get node -o wide --no-headers | awk '{print $6}' | head -1)
sleep 120
podman run --rm -it -e HOST_IP=$HOST_IP {{ api_env }} {{ ingress_env }} quay.io/karmab/contrail-allow-vips:latest
return 0
}

export KUBECONFIG=/opt/openshift/auth/kubeconfig
while ! patchfunc; do
    echo "Waiting 10s to retry..."
    sleep 10
done
touch kcli-contrail-patch.done
