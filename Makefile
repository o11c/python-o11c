PYTHON := python3

test:


COVERAGE := ${PYTHON} -m coverage
COVER := ${COVERAGE} run -p --source=.

test-coverage: test-unittest
test-unittest: clean-coverage
	${COVER} -m unittest

test: test-copyright
test-copyright:
	find -name '*.py' -print0 | xargs -0 -n 1 grep -L -w Copyright

test: test-coverage
test-coverage:
	${COVERAGE} combine
	${COVERAGE} html
	${COVERAGE} report --fail-under=100

clean-coverage:
	rm -f .coverage*
	rm -rf htmlcov
