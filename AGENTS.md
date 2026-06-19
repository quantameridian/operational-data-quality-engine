This repository is a public technical portfolio project focused on operational data quality, exception management, reporting assurance, and Python analytical development.

## Working rules

- Keep changes narrow and intentional.
- Do not introduce delivery claims, sensitive data, employer-owned material, or exaggerated outcomes.
- Use only realistic non-client sample data.
- Prefer simple, readable architecture over unnecessary complexity.
- Do not create generic tutorial-style content.
- Do not overuse buzzwords.
- Do not rewrite the whole repository unless explicitly requested.
- Keep documentation consistent with the actual code.
- Add tests for meaningful business rules.
- Maintain a clear run path for a reviewer cloning the repo.

## Code standards

- Use clear module boundaries.
- Prefer explicit names over clever abstractions.
- Avoid one large script.
- Avoid excessive comments explaining obvious code.
- Include type hints where helpful.
- Keep generated outputs reproducible.
- Prefer small, testable functions.
- Use meaningful test cases based on business rules.
- Keep rule outputs easy to trace back to the source record and rule ID.

## Documentation standards

This repo should explain:

- the business problem
- the data route
- the architecture
- how to run locally
- what outputs are produced
- what is tested
- what is not covered
- how this would translate to a real organisation
- which rules exist and why they matter

## Verification

Before considering a task complete, check:

- formatting
- linting
- tests
- README accuracy
- sample output generation
- no sensitive data
- no unsupported delivery claims
- no generic filler copy
- no outputs that were invented by hand
