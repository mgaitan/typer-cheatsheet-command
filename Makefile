.PHONY: install
export UV_MALWARE_CHECK := 1

install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@if command -v prek >/dev/null 2>&1; then \
		echo "🪝 Installing git hooks with prek"; \
		prek install; \
	else \
		echo "ℹ️  prek is not installed. Install it with: uv tool install prek"; \
	fi

.PHONY: test qa
test: ## Run tests with coverage
	@echo "🧪 Running tests with coverage"
	@uv run pytest

qa: ## Run local QA checks via prek
	@if command -v prek >/dev/null 2>&1; then \
		echo "🔍 Running prek checks"; \
		prek run --all-files; \
	else \
		echo "ℹ️  prek is not installed. Install it with: uv tool install prek"; \
	fi

.PHONY: bump
bump:
	uv version --bump minor

.PHONY: release
release: ## Create a GitHub release for the current version
	@version=$$(uv version --short); \
	git commit -am "Bump $$version"; \
	git push origin main; \
	owner=$$(gh repo view --json owner -q .owner.login); \
	gh api repos/{owner}/{repo}/releases/generate-notes -f tag_name="$$version" --jq .body \
		| sed "s/ by @$$owner\$$//g; s/ by @$$owner / /g" \
		| gh release create "$$version" --notes-file -

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_.-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
