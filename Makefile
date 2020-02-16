all: reqs cvrg build sscas

reqs:
	pip install -r requirements.txt

test:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/python3 -m unittest

cvrg:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/coverage run --branch --source=. -m unittest && \
	`pwd`/venv/bin/coverage report --ignore-errors --omit=venv/**,tests/**,*__init__* && \
	`pwd`/venv/bin/coverage xml

sscas:
	sonar-scanner -Dsonar.projectKey=pOm

build:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/python3 setup.py sdist bdist_wheel
	# `pwd`/venv/bin/python3 setup.py sdist bdist_wheel

armor:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/pyarmor build -B

run:
	export PYTHONPATH=`pwd`/venv/bin/python3
	python3 scripts/patternomatic.py hola
