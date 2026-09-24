# CLAUDE.md

`secure-aks` is a personal purple-team lab around **CVE-2025-55182** ("React2Shell").
What it is, the phases, and per-phase steps/commands live in [docs/](docs/)
(overview in [docs/PLAN.md](docs/PLAN.md)).

## Intentionally vulnerable code

Some code is *meant* to be insecure (the pinned Next.js app, over-privileged RBAC
and node identity). Do **not** "fix" these — they are the experiment. Hardening
happens in its own phases, each validated by re-running the attack.

## Safety

Personal lab only. Never expose the vulnerable app to the internet — this CVE is
exploited in the wild. Keep it on local `kind` or a private AKS cluster.

## Conventions

- **Docs:** numbered phase files in `docs/`, each opening with a `[Back](../README.md)`
  link, a table of contents, then a step table.
- **Infra:** Terraform; state, `.tfvars`, `.terraform/` stay untracked.
- **Deploy:** GitOps via Argo CD, app-of-apps pattern.
