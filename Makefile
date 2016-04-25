init:
	pip install -r requirements-dev.txt

develop:
	pip install --editable .

install:
	pip install .

test:
	nosetests -v tests
