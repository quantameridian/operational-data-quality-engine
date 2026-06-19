# Contributing

This repository is primarily a portfolio artifact, but contributions and review
comments are welcome if they improve clarity, correctness, or reproducibility.

## Before opening a pull request

1. Keep all data synthetic and non-client.
2. Keep generated/cache folders out of Git.
3. Run:

   ```bash
   make test
   make lint
   make run
   ```

4. Update README or docs when behavior changes.
5. Explain the business reason for the change, not only the technical edit.

## Review standard

A change is not ready if it makes the project look more polished while reducing
truthfulness, reproducibility, or reviewer confidence.
