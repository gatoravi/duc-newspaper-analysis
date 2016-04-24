init:
	pip install -r requirements-dev.txt --use-mirrors

install:
	pip install .

test:
	nosetests -v tests
