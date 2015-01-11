.PHONY: test autotest

test:
	nosetests

autotest:
	nosetests --with-watch
