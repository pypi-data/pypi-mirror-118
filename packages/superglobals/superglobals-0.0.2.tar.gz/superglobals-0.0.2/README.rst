Easy access to globals() from inside a python module.

See: https://stackoverflow.com/questions/15959534/visibility-of-global-variables-in-imported-modules/69029612#69029612

Using superglobals
============

.. code-block:: python

    import superglobals
    
    from superglobals import *

    superglobals()[var] = value

    setglobal('test', 123)
    defaultglobal('test', 456)
    assert(getglobal('test') == 123)


Changelog
=========

0.0.1: initial release (2021-09-02)
0.0.2: this document (2021-09-02)

