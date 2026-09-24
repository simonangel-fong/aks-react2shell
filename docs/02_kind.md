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

```sh

```
