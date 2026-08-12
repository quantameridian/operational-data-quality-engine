# Security Posture

## Public data boundary

Normal execution needs no network connection, credential, token, or private endpoint. Every committed record is synthetic. Real operational data, internal URLs, tenant identifiers, credentials, certificates, and personal information must not enter this repository.

## Repository controls

- GitHub Actions receive read only repository contents permission.
- Third party actions are pinned to full commit hashes.
- CI runs Ruff, the test and coverage gate, `pip-audit`, the sample engine, and a scale smoke check.
- CodeQL scans Python changes.
- OpenSSF Scorecard reviews repository and supply chain settings.
- Dependabot checks Python and GitHub Actions dependencies.
- `SECURITY.md` routes vulnerability reports away from public issues.
- Local databases, environments, caches, logs, editor files, and build outputs are ignored.

## Input handling

CSV files use the Python standard library parser and must match the required header contract. DuckDB input uses a read only connection. Table names accept only letters, numbers, and underscores before they are included in SQL. Values are selected through a fixed field list.

These controls do not make arbitrary untrusted files harmless. Run unknown data in an isolated environment with resource limits. Do not expose the local CLI directly as a network service.

## Provenance

The run manifest records SHA256 hashes for the source, rule policy, and generated text outputs. This supports comparison and review. It is not a signed attestation and does not prove who supplied or approved a file.

## GitHub settings

Keep secret scanning, push protection, Dependabot alerts, security updates, private vulnerability reporting, and read only default workflow tokens enabled. Protect `main` with required CI checks, blocked force pushes, and blocked deletion when the repository plan supports rulesets for a private owner account.

## Residual risk

There is no authentication, authorisation, encryption service, sandbox, rate limit, scheduler, alert route, or incident integration. Dependencies are version bounded but not locked with hashes. A production deployment needs a threat model, approved data classification, least privilege access, secret management, patch ownership, logging, retention, recovery, and independent security review.
