SHELL := /bin/bash
COMPOSE := openlineage-marquez.yml
PY := python
PIP := python -m pip

# Defaults you can override: `make demo OPENLINEAGE_NAMESPACE=sandscript-ai`
OPENLINEAGE_URL ?= http://localhost:3000
OPENLINEAGE_NAMESPACE ?= ai-apps
OPENLINEAGE_APP_NAME ?= Sandscript AI LLM

# ---- Docker / Marquez ----
up:
	docker compose -f $(COMPOSE) up -d --force-recreate --remove-orphans

down:
	docker compose -f $(COMPOSE) down -v

ps:
	docker compose -f $(COMPOSE) ps

logs:
	docker compose -f $(COMPOSE) logs -f marquez

health:
	./scripts/health.sh

# ---- Python / Tests / Demo ----
venv:
	python3 -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip
	. .venv/bin/activate && $(PIP) install -e ".[langchain,litellm]" pytest

test:
	. .venv/bin/activate && pytest -q

demo:
	. .venv/bin/activate && \
	OPENLINEAGE_URL='$(OPENLINEAGE_URL)' \
	OPENLINEAGE_NAMESPACE='$(OPENLINEAGE_NAMESPACE)' \
	OPENLINEAGE_APP_NAME='$(OPENLINEAGE_APP_NAME)' \
	$(PY) examples/custom_pipeline.py

# ---- Packaging / Release helpers ----
version ?= 0.1.0
tag:
	git tag v$(version)
	git push origin v$(version)

sdist:
	. .venv/bin/activate && $(PY) -m build

zip:
	git ls-files > /tmp/filelist && zip -r "openlineage-llm-$(version).zip" -@ < /tmp/filelist && rm /tmp/filelist
