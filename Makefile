#
# PatternOmatic Makefile
#
export PYTHONPATH=.

all: reqs cvrg build sscas

venv:
	source venv/bin/activate

clean:
	rm -rf `pwd`/build
	rm -rf `pwd`/dist
	rm -rf `pwd`/PatternOmatic.egg-info

reqs:
	pip install -r requirements.txt

test:
	python -m unittest

cvrg:
	coverage run --branch --source=. -m unittest && \
	coverage report --ignore-errors --omit=venv/**,tests/**,*__init__* && \
	coverage xml

sscas:
	sonar-scanner -Dsonar.projectKey=pOm

build:
	python setup.py sdist bdist_wheel

armor:
	pyarmor build -B

run:
	python ./scripts/patternomatic.py -s hello Mr. Puffin -s Goodbye Mrs. Muffin
