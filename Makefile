#
# PatternOmatic Makefile
#
export PYTHONPATH=.

all: libs coverage clean build sonar

venv:
	source venv/bin/activate

clean:
	rm -rf `pwd`/build
	rm -rf `pwd`/dist
	rm -rf `pwd`/PatternOmatic.egg-info
	rm -rf `pwd`/fil-result

libs:
	pip install -r requirements.txt

test:
	python -m unittest

coverage:
	coverage run --branch --source=PatternOmatic,scripts,tests --omit=*__init__* -m unittest && \
	coverage report --ignore-errors --omit=venv/**,tests/**,*__init__* && \
	coverage xml

sonar:
	sonar-scanner -Dsonar.projectKey=pOm -Dsonar.exclusions=tests/**

sonarcloud:
	sonar-scanner -Dsonar.projectKey=revuel_PatternOmatic

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload -u __token__ -p ${PYPI_TOKEN} --repository-url https://upload.pypi.org/legacy/ dist/*

run:
	python ./scripts/patternomatic.py -s Hello Mr. Puffin -s Goodbye Mrs. Muffin
