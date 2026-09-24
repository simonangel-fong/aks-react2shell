# kind cluster

[Back](../README.md)

- [kind cluster](#kind-cluster)
  - [Steps](#steps)
  - [Create kind](#create-kind)
  - [argocd and manifest](#argocd-and-manifest)

---

## Steps

| #   | Steps               | Step                      |
| --- | ------------------- | ------------------------- |
| 1   | create kind cluster | create kind cluster       |
| 2   | argocd              | create argocd app-of-apps |
| 3   | create secret       | dummy crown jewels        |

## Create kind

Cluster config: [../kind/kind-config.yaml](../kind/kind-config.yaml)
(1 control-plane + 2 workers, with host port mappings for the app and Argo CD).

```sh
# Create the cluster from the pinned config.
kind create cluster --config kind/kind-config.yaml

# Verify: context, nodes Ready, system pods running.
kubectl config use-context kind-secure-aks
kubectl get nodes -o wide
kubectl get pods -A

# clean up
# kind delete cluster --name secure-aks
```

## argocd and manifest

GitOps via Argo CD, app-of-apps.

```txt
argocd/
  root-app.yaml                    # app-of-apps root (apply by hand)
  apps/react2shell.yaml            # child Application
  manifests/react2shell/           # the vulnerable app (ns, deployment, service)
```

```sh
# ##############################
# install argocd
# ##############################
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update argo
# Hang tight while we grab the latest from your chart repositories...
# ...Successfully got an update from the "argo" chart repository
# Update Complete. ⎈Happy Helming!⎈

# install argocd
helm install argocd argo/argo-cd --namespace argocd --create-namespace

# get pwd
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode; echo
# port forward
kubectl port-forward service/argocd-server -n argocd 8080:443

# ##############################
# deploy app-of-apps
# ##############################
git add argocd
git commit -m "argocd: app-of-apps + react2shell manifests"
git push

kubectl apply -n argocd -f argocd/root-app.yaml

# Verify + get UI login (user: admin, URL: http://localhost:8443).
kubectl -n argocd get applications
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d; echo
```
