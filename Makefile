#
# patternomatic Makefile
#
# This file is part of patternomatic.
#
# Copyright © 2020  Miguel Revuelta Espinosa
#
# patternomatic is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# patternomatic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with patternomatic. If not, see <https://www.gnu.org/licenses/>.
#
export PYTHONPATH=.

all: libs coverage clean build sonar

venv:
	source venv/bin/activate

clean:
	rm -rf `pwd`/build
	rm -rf `pwd`/dist
	rm -rf `pwd`/patternomatic.egg-info
	rm -rf `pwd`/fil-result

libs:
	pip install -r requirements.txt

test:
	python -m unittest

coverage:
	coverage run --branch --source=patternomatic,scripts,tests --omit=*__init__* -m unittest && \
	coverage report --ignore-errors --omit=venv/**,tests/**,*__init__* && \
	coverage xml

sonar:
	sonar-scanner -Dsonar.projectKey=pOm -Dsonar.exclusions=tests/**

sonarcloud:
	sonar-scanner -Dsonar.projectKey=revuel_patternomatic

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload -u __token__ -p ${PYPI_TOKEN} --repository-url https://upload.pypi.org/legacy/ dist/*

run:
	python ./scripts/patternomatic.py -s Hello Mr. Puffin -s Goodbye Mrs. Muffin
