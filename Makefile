lint:
	flake8 setup.cfg
	isort --check --diff pyproject.toml
	black --check pyproject.toml

format:
	isort pyproject.toml
	black pyproject.toml
