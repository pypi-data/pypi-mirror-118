================
pytest-nogarbage
================

.. image:: https://img.shields.io/pypi/v/pytest-nogarbage.svg
    :target: https://pypi.org/project/pytest-nogarbage
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-nogarbage.svg
    :target: https://pypi.org/project/pytest-nogarbage
    :alt: Python versions

.. image:: https://travis-ci.org/mvollrath/pytest-nogarbage.svg?branch=master
    :target: https://travis-ci.org/mvollrath/pytest-nogarbage
    :alt: See Build Status on Travis CI

The purpose of this plugin is ensuring that portions of your Python code do not produce garbage or manually invoke garbage collection.

When the `nogarbage` pytest fixture is added to a test, it will cause an error under the following conditions:

* Garbage was collected after the test was run (circular references were remaining after the test was broken down).
* Garbage was explicitly collected  (`gc.collect()`) during the test.  Automatic garbage collection sweeps are disabled during the test.

You should use this plugin when:

* You intend to run a program with garbage collection disabled in production.
* You wish to verify elimination of garbage collection overhead produced by frequently called functions.


Requirements
------------

* Python 3.7+
* This plugin is only tested against CPython.


Installation
------------

You can install "pytest-nogarbage" via `pip`_ from `PyPI`_::

    $ pip install pytest-nogarbage


Usage
-----

Add the `nogarbage` fixture to your test to ensure it does not produce garbage::

    def test_circular(nogarbage):
        l1 = []
        l2 = [l1]
        l2.append(l1)
        # ERROR: Garbage collected after test.

    def test_collect(nogarbage):
        import gc
        gc.collect()
        # ERROR: Garbage collected during test.


Recommended Reading
-------------------

If you are interested in optimizing CPython garbage collection, the `gc docs`_ and `CPython Garbage Collection devguide`_ are excellent resources.


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-nogarbage" is free and open source software.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/mvollrath/pytest-nogarbage/issues
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`gc docs`: https://docs.python.org/3/library/gc.html
.. _`CPython Garbage Collection devguide`: https://devguide.python.org/garbage_collector/
