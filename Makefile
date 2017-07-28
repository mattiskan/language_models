.PHONY: run test clean eval

NLTK_DATA="$(HOME)/nltk_data"

run: venv
	venv/bin/python src/main.py

generate: venv
	venv/bin/python src/generator.py

test: venv
	venv/bin/python -m pytest -v tests/

eval: venv .nltk_data
	venv/bin/python src/evaluate_model.py

.nltk_data:
	venv/bin/python -m nltk.downloader -d $(NLTK_DATA) all
	ln -s $(NLTK_DATA) .nltk_data # create target to prevent re-download

clean:
	rm -rf venv/
	rm .nltk_data
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

venv: requirements.txt
	if [ ! -d venv ]; then virtualenv -p `which python3.6` venv; fi
	venv/bin/pip install -r requirements.txt

	@echo 'Build done. You may want to activate the virtualenv:\nsource venv/bin/activate'
