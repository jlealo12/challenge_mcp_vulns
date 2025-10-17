CURRENT_VERSION = $(shell uv version --short)
version:
	uv version --bump patch

tag:
	echo "Tagging version $(CURRENT_VERSION)"
	git tag -am "Release v$(CURRENT_VERSION)" "v$(CURRENT_VERSION)"
	
commit-tag:
	git add pyproject.toml uv.lock
	git commit -m "tag: update version tag"

push:
	git push &&	git push --tags

run-agent:
	clear
	@echo "Executing agent..."
	uv run agent/main.py

mcp:
	clear
	@echo "Running MCP server..."
	uv run mcp/main.py

test-mcp:
	clear
	@echo "Testing MCP server..."
	uv run mcp/client.py