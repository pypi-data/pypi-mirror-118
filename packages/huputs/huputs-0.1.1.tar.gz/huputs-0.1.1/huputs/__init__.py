"""
HUPUTS: Human-Understandable Python Unit Test System

a behavior-driven development framework in Python.
By the IFD.

Functions
---------
run(path: str, d: str = ".")
    Runs unit tests from a dir or file path.
empty(cls)
    Make `cls`'s __init__ empty.

Classes
-------
TestThingsOut
    The unit test system.
Call
    For storing call records for injected functions.
Test
    For storing tests

Raises
------
BadArgumentError
    A bad argument has passed into a function call of huputs.
TestError
    During a test, something is unexpected.
"""
from .system import BadArgumentError, Call, Test, TestError, TestThingsOut, run
from .utils import empty
