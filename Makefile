.PHONY: run test clean eval

NLTK_DATA="$(HOME)/nltk_data"

start_webserver: build
	venv/bin/python src/web_interface.py

run: build
	venv/bin/python src/main.py

generate: build
	venv/bin/python src/generator.py

test: build
	venv/bin/python -m pytest -v tests/

eval: build
	venv/bin/python src/evaluate_model.py

crawl: build
	venv/bin/python src/crawler.py

clean:
	rm -rf venv/
	rm .nltk_data
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

build: venv .nltk_data

.nltk_data: # can't be dependency of venv because that would invalidate `touch .nltk_data`
	venv/bin/python -m nltk.downloader -d $(NLTK_DATA) all
	ln -s $(NLTK_DATA) .nltk_data # create target to prevent re-download

venv: requirements.txt
	if [ ! -d venv ]; then virtualenv -p `which python3.6` venv; fi
	venv/bin/pip install -r requirements.txt

	@echo 'Build done. You may want to activate the virtualenv:\nsource venv/bin/activate'
