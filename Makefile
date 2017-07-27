.PHONY: run test clean

run: venv
	venv/bin/python src/main.py

test: venv
	venv/bin/python -m pytest -v tests/

clean:
	rm -rf venv/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

venv: requirements.txt
	if [ ! -d venv ]; then virtualenv -p `which python3.6` venv; fi
	venv/bin/pip install -r requirements.txt

	@echo 'Build done. You may want to activate the virtualenv:\nsource venv/bin/activate'
