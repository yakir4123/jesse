install:
	pip install uv
	uv venv
	uv pip install -r requirements_rl.txt

dev:
	PYTHONPATH=. uv run python jesse/rl/main.py

test:
	uv run python -m pytest tests/test_rl_strategy.py::TestRLStrategy::test_rl_strategy