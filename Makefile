all:
	reqs, cvage, build
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
sscas:
	sonar-scanner -Dsonar.projectKey=pOm
build:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/python3 setup.py sdist bdist_wheel
armor:
	export PYTHONPATH=`pwd`/venv/bin/python3
	`pwd`/venv/bin/pyarmor build -B
	# cd dist/PatternOmatic
	# python main.py
