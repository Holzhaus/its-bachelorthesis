# xjcc - XML/JSON conversion checker
## Prerequisites
Other than Python >= 3.5 you need these libraries:

- [setuptools](https://pypi.python.org/pypi/setuptools)
- [defusedxml](https://pypi.python.org/pypi/defusedxml)
- [lxml](http://lxml.de)

All of them can be installed via `pip`:

    $ pip install --user setuptools defusedxml lxml

Please note that each converter plugin might have additional dependencies.

## Installation

Just use the `install` command of `setup.py`:

    $ ./setup.py install --user

## Unittests

To run unittests, just put this into a terminal and hit enter:

    $ ./setup.py test

If you have the [coverage](https://pypi.python.org/pypi/coverage) library
installed, you can also use:

    $ python -m coverage run ./setup.py test

In that case, you can get a code coverage report:

    $ python -m coverage report
