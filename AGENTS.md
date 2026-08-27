Project: Typer Cheatsheet Command

Repository: https://github.com/mgaitan/typer-cheatsheet-command

Description: A pluggable cheatsheet command for Typer applications.

## Project Scope

- This repository is generated from `mgaitan/python-package-copier-template`.
- Keep local project code, docs, CI, and release automation aligned with the template defaults unless the project has an intentional reason to diverge.
- When updating from the template, review generated changes carefully and preserve project-specific behavior.
- `mgaitan/yet-another-demo` is the canonical example repository for this template. Use experiment branches there when validating template behavior before adopting it here.

## Stack

- **Python:** Python 3.14. Check main dependencies in `pyproject.toml`.
- **Tests:** pytest and pytest-cov. `make test` to run tests, or `uv run pytest`.
- **Productivity:** Dependencies managed with `uv` via `pyproject.toml`;
- **lint/format:** Ruff.
- **Git:** and GitHub

## Python preferences

- Modern and idiomatic practices that emphasize clarity and predictable behavior. Examples of modern features:
   - Pathlib for file operations
   - Data model methods (like __len__, __add__, etc.)
   - Stdlib or pydantic dataclasses
   - Advanced itertools
   - Pattern matching
   - Walrus operator
   - Enums subclasses
- Dependency changes use `uv add` or `uv remove`
- Use `uv run - <<'PY' ...` instead `python - <<'PY'` for inline scripts
- Docstrings in Markdown ("myst") format, expressing intentions rather than implementation details.
  Make references to other code if appropriate. Eg: "See also `{py:func}`other_module.helper_function`.".
- Explicit and robust type annotations using built-in generics (`list`, `dict`, etc.), union types with `|`, etc.
- Validate type safety with `uv run ty check` after relevant code changes.
- Prefer flat code: use early returns, guard clauses, fixtures over context managers on tests, etc.
- Never hallucinate APIs or behaviours. If uncertain, inspect the code and/or check online documentation (ensure it's the correct version declared by uv.lock) or ask the developer

## Git/GitHub preferences

- Ensure you are in a proper branch for each new feature or bugfix.
- Never commit or push automatically unless instructed otherwise.
- Prefer `gh` CLI for all interactions with GitHub if possible. Eg. Use it to open PRs / manage issues.
- For `gh pr` interactions, prefer `--body-file` with a temporary file created under `/tmp/`.
- To request review from a specific user or agent, use `gh`; for example, `gh pr edit --add-reviewer @copilot`.
- When a repository defines release targets in `Makefile`, prefer those targets over ad-hoc release commands. Use the repository's release target to run checks and publish a release. When preparing a version-bump PR, use its bump target.
- For issue categorization, use GitHub labels instead of title prefixes like `Bug:`, `Feat:`, or `Docs:`.
- Before assigning labels, inspect labels already used in the target repository and follow that taxonomy first.
- If labels are missing or incomplete, use this baseline set: `bug`, `enhancement`, `documentation`, `maintenance`, `refactor`, `test`, `ci`, `dependencies`, `security`, `performance`, `ux`, `question`.
- Consider mentioning yourself in the commits as co-author if you helped enough. Use the standard Git co-author trailer:
  "Co-authored-by: Name <email>".
  For common AI collaborators, use:
  - "Co-authored-by: codex <codex@openai.com>".
  - "Co-authored-by: Claude <noreply@anthropic.com>".

## Documentation

The README is the project's public documentation. Keep installation, integration,
and behavior examples current when the package changes.

## Language preferences

- The public language is English: all committable text and GitHub interactions must be in simple English (including documentation, comments, docstrings, commit messages, PR descriptions, etc.).
- However, when interacting with the developer in chat, respond in the language they use.
- Avoid sexist or exclusionary language. Always prefer gender-neutral phrasing.
