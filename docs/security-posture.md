# Security Posture

## Scope

This is a public portfolio repository. All committed files must be safe for full
public review. The project uses synthetic data only and must not contain client
data, employer data, credentials, tokens, private URLs, or internal system names.

## Current Controls

- GitHub Actions CI uses read-only repository contents permission.
- Python dependency checks target Python 3.11 or newer so fixed tooling
  versions are installable.
- Python dependencies are audited in CI with `pip-audit`.
- CodeQL scans the Python code path.
- OpenSSF Scorecard runs on the public repository and uploads SARIF results.
- Dependabot version updates are configured for Python and GitHub Actions.
- Security reporting instructions are documented in `SECURITY.md`.
- Generated cache and local environment folders are excluded by `.gitignore`.

## Data and Secret Boundary

The engine reads synthetic CSV files from `data/` and writes generated sample
outputs to `outputs/` and `docs/`. It does not require secrets, API tokens,
database credentials, or network access for normal execution.

Do not commit:

- real operational trackers;
- customer, employer, or client data;
- API keys, passwords, tokens, certificates, or private keys;
- internal hostnames, tenant IDs, or private repository URLs;
- local virtual environments, caches, coverage output, or build artifacts.

## GitHub Settings To Keep Enabled

These controls live in GitHub repository settings rather than source files:

- secret scanning and push protection;
- Dependabot alerts and Dependabot security updates;
- branch protection or repository rulesets for `main`;
- required CI checks before merging;
- blocked force pushes and branch deletion;
- default workflow token permission set to read-only.

## Residual Risk

This repository demonstrates a small batch data-quality engine. It is not a
production service, does not implement authentication, and does not protect live
systems. Security review should focus on supply-chain hygiene, public-data
boundaries, generated-output safety, and whether the repository avoids leaking
sensitive information.
