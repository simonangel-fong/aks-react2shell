# React2Shell to AKS

**Goal:** Prove security skill end-to-end on one real CVE — exploit it, detect it, harden it, then prove containment. Purple-team lifecycle mapped to CKS domains.

**CVE:** CVE-2025-55182 ("React2Shell") — unauthenticated RCE in React Server Components (CVSS 10.0), triggered by a single crafted POST.

> Personal lab only. Never expose the vulnerable app to the internet — this CVE is exploited in the wild.

## Repository layout

```txt
secure-aks/
  app/                react app source code
  argocd/             argocd, app-of-apps, k8s manifests
  kind/               kind cluster for local dev
  infra/
    project/          project-level terraform code
    aks/              aks terraform code
  docs/               documentation
  README
```

## Phases

| #   | Phase          | Description                                                                |
| --- | -------------- | -------------------------------------------------------------------------- |
| 1   | vulnerable app | A simple Next.js web app with React2Shell-vulnerable version; Dockerfile.  |
| 2   | local kind     | A kind cluster; setup Argo CD and Kubernetes manifests; dummy crown jewels |
| 3   | local breach   | Exploit the app and retrieve crown jewels; document attack chain           |
| 4   | Detect         | Deploy grafana+loki; set alert; verify attack                              |
| 5   | Harden cluster | harden cluster                                                             |
| 6   | Harden pod     | harden pod                                                                 |
| 7   | Harden app     | Harden app                                                                 |
| 8   | shift left     | create github actions workflow                                             |
| 9   | AKS vulnerable | Create AKS wiwth terraform, argo cd, and vulnerable deployment             |
| 10  | aks harden     | create shift left cicd to secure aks                                       |

**Crown jewels (escalating blast radius)**

- **Pod** — a Secret mounted into the app pod (reached by RCE alone).
- **Cluster** — PostgreSQL credentials Secret in the `db` namespace (reached via stolen ServiceAccount token → RBAC).
- **Cloud** — production DB creds in Azure Key Vault (reached via IMDS → over-privileged node identity).
- _Host/node tier deferred_ (AKS abstracts host config).

**Validation:** After each hardening step, re-run the attack. Which crown jewels can still be stolen: pod, cluster, or cloud?

**Hardening layers:**

- App: patch, non-root, distroless
- Pod: securityContext, seccomp
- Cluster: PSS restricted, least-priv RBAC, egress NetworkPolicy, Kyverno
- Infra: Workload Identity, block IMDS, private API, Defender
