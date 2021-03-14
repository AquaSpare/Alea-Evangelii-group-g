##
# Communication Platform
#
# @file
# @version 0.1

.PHONY = test

test:
	mypy .
	python3 -m unittest

# end
