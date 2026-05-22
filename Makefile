PLUGIN_NAME := sharebird-unicorn-canvas
VERSION := $(shell python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
DIST_DIR := dist
ARTIFACT := $(DIST_DIR)/$(PLUGIN_NAME)-v$(VERSION).zip

.PHONY: help validate plugin install clean smoke ingest-smoke smoke-all

help:
	@echo "Targets:"
	@echo "  make validate      Validate plugin.json + SKILL.md frontmatter"
	@echo "  make plugin        Build $(ARTIFACT)"
	@echo "  make install       Symlink the skill into ~/.claude/skills/ for local use"
	@echo "  make smoke         Run fill_canvas.py with a sample payload"
	@echo "  make ingest-smoke  Run ingest_inputs.py against fixture files"
	@echo "  make smoke-all     Run both smoke tests"
	@echo "  make clean         Remove dist/"

validate:
	@python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); print('plugin.json OK')"
	@test -f skills/$(PLUGIN_NAME)/SKILL.md && echo "SKILL.md OK" || (echo "MISSING skills/$(PLUGIN_NAME)/SKILL.md"; exit 1)
	@test -f skills/$(PLUGIN_NAME)/templates/canvas-blank.xlsx && echo "canvas-blank.xlsx OK" || (echo "MISSING blank template"; exit 1)
	@test -f skills/$(PLUGIN_NAME)/references/rubric.md && echo "rubric.md OK" || (echo "MISSING rubric"; exit 1)
	@test -f skills/$(PLUGIN_NAME)/scripts/fill_canvas.py && echo "fill_canvas.py OK" || (echo "MISSING fill_canvas.py"; exit 1)

plugin: validate
	@mkdir -p $(DIST_DIR)
	@rm -f $(ARTIFACT)
	@zip -r $(ARTIFACT) .claude-plugin skills LICENSE README.md CHANGELOG.md \
		-x "*.DS_Store" -x "*__pycache__*" -x "*.pyc" -x "dist/*" >/dev/null
	@echo "Built $(ARTIFACT)"

install:
	@mkdir -p $$HOME/.claude/skills
	@ln -snf "$$(pwd)/skills/$(PLUGIN_NAME)" $$HOME/.claude/skills/$(PLUGIN_NAME)
	@echo "Linked $$HOME/.claude/skills/$(PLUGIN_NAME) -> $$(pwd)/skills/$(PLUGIN_NAME)"

smoke:
	@python3 scripts/smoke_fill_canvas.py

ingest-smoke:
	@python3 scripts/smoke_ingest_inputs.py

smoke-all: smoke ingest-smoke

clean:
	rm -rf $(DIST_DIR)
