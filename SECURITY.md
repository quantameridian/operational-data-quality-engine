# Security Policy

## Report privately

Do not open a public issue for a suspected vulnerability, leaked secret, or sensitive data exposure. Use [GitHub private vulnerability reporting](https://github.com/quantameridian/operational-data-quality-engine/security/advisories/new), or contact the repository owner through the GitHub profile.

Include the affected version or commit, safe reproduction steps, expected impact, and any suggested correction. Do not include a working secret or real personal data in the report.

## Supported version

Security corrections apply to the current `main` branch. There are no supported release branches or deployed service versions.

## Data boundary

This repository is a local reference implementation with synthetic data. It is not approved for protected, client, employee, or operational data. A production use needs a separate security and data protection review.

See the [security posture](docs/security-posture.md) for implemented controls and residual risks.
