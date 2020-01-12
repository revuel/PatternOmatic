all:
	reqs, test, cover, build
reqs:
	pip install -r requirements.txt
test:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/python3 -m unittest
cvage:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/coverage run --branch --source=. -m unittest && \
	`pwd`/venv/bin/coverage report --ignore-errors --omit=tests/**,*__init__* && \
	`pwd`/venv/bin/coverage xml
build:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/python3 setup.py sdist bdist_wheel
