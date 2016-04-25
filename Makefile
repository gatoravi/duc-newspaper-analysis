.PHONY: init develop install test clean

init:
	pip install -r requirements-dev.txt

develop:
	pip install --editable .

install:
	pip install .

test:
	nosetests -v tests

clean:
	find newsponder -name "*.pyc" -exec rm -v {} \;
