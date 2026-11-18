# Commands we'll use throughout the project
## Task
- Initialize project  uv init --bare
- Create environment	uv venv --python 3.11
- Add dependency	uv add package-name
- Add development dependency	uv add --dev pytest
- Run Python script	uv run python script.py
- Run tests	uv run pytest
- Check code quality	uv run ruff check .
- Synchronize dependencies	uv sync
- Update a package	uv lock --upgrade-package package-name