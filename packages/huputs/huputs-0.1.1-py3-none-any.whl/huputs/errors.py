"""
Custom errors/exceptions are here.

Classes
-------
TestError
    During a test, something is unexpected.
BadArgumentError
    A bad argument has been passed into a function call of huputs.
"""


class TestError(Exception):
    """During a test, something is unexpected."""
    pass


class BadArgumentError(Exception):
    """A bad argument has been passed into a function call of huputs."""
    pass
