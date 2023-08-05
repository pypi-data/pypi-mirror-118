"""
System of huputs.

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
    For storing tests.

Raises
------
TestError
    During a test, something is unexpected.
BadArgumentError
    A bad argument has passed into a function call of huputs.
"""
import asyncio
import functools
import logging
import os
import typing
from dataclasses import dataclass

from . import ex
from .errors import BadArgumentError, TestError
from .utils import diff, tidy_fn_call, to_dict, visualise

logger = logging.getLogger("HUPUTS")


def calc_coverage(i: ex.Interacter):
    uncovered = {}
    for fname, lns in i.coverage.items():
        if not ex.file_in_dir(fname, i.src):
            continue
        f = open(fname, "r")
        uncovered[fname] = ""
        for n, l in enumerate([l.strip() for l in f.readlines()]):
            if n not in lns:
                if uncovered[fname].endswith(f"-{n}"):
                    uncovered[fname] = uncovered[fname][
                        : -len(uncovered[fname].split()[-1].split("-")[1])
                    ] + str(n + 1)
                elif uncovered[fname].endswith(f" {n}") or uncovered[
                    fname
                ] == str(n):
                    uncovered[fname] += f"-{n+1}"
                elif not uncovered[fname]:
                    uncovered[fname] += str(n + 1)
                else:
                    uncovered[fname] += f" {n+1}"
        f.close()
    return uncovered


def run(path: str, d: str = None, cwd: str = None):
    """
    Runs unit tests from a dir or file path.

    Parameters
    ----------
    path : str
        The path to the dir/file
    d : str, optional
        The dir with the scripts for coverage calculations, by default cwd.
    cwd : str, optional
        The working directory to run the test scripts, by default cwd.

    Raises
    ------
    BadArgumentError
        The path is invalid
    """
    _cwd = os.getcwd()
    d = d or _cwd
    cwd = cwd or _cwd
    if os.path.isfile(path):
        if not path.endswith(".py"):
            return
        i = ex.Interacter(d)
        print(f"Running {path}…")
        l = i.test_out(path, cwd)
        if l:
            print(l)
        # FIXME coverage system
        # print("Coverage:")
        # for fname, s in calc_coverage(i).items():
        #     print(os.path.relpath(fname), s)
    elif os.path.isdir(path):
        for file in os.listdir(path):
            run(os.path.join(path, file))
    else:
        raise BadArgumentError(f"invalid path {path}")


@dataclass
class Test:
    """
    For storing tests.

    Create a test using TestThingsOut.add_test()

    Attributes
    ----------
    chk_fn : typing.Callable
        The check function
    for_fn : typing.Callable
        The function to be checked
    executor : typing.callable
        The executor that calls `chk_fn`
    """

    chk_fn: typing.Callable
    for_fn: typing.Callable
    executor: typing.Callable

    @property
    def __call__(self):
        return self.chk_fn


@dataclass
class Call:
    """
    For storing call records for injected functions.

    This class is automatically constructed by `dataclasses.dataclass`.
    Some args will be automatically moved to `kws` from `args`.

    Attributes
    ----------
    name : str
        Name of the function being called
    args : list
        List of arguments, equivalent to the *args parameter
    kws : dict
        The keyword argumets, equivalent to the **kwargs parameter
    ret : typing.Any, optional
        The return value of the call
    """

    name: str
    args: list
    kws: dict
    ret: typing.Any = None


class TestThingsOut:
    """
    The huputs unit test system.

    Make each new instance of this in a test script

    Attributes
    ----------
    tests : dict[str, Test]
        The tests added by add_test()
    the_executor : typing.Coroutine
        The global executor

    Methods
    -------
    execute_tests_like_this(fn: typing.Callable) -> typing.Callable
        Decorator for saving the global executor
    how_to_execute(test_name: str) -> typing.Callable
        Decorator for saving executor for a test
    """

    tests: dict[str, Test] = {}
    _current_res: list[Call] = []

    @staticmethod
    async def the_executor(chk_fn: typing.Callable):
        """
        Directly awaits chk_fn.

        Parameters
        ----------
        chk_fn : Callable
            the check Callable

        Returns
        -------
        Optional[Any]
            The value returned by `chk_fn`, or None if `chk_fn` errors out.
        """
        if asyncio.iscoroutinefunction(chk_fn):
            return await chk_fn()
        return chk_fn()

    def execute_tests_like_this(self, fn: typing.Callable) -> typing.Callable:
        """
        Decorator for saving the global executor

        The executor will be saved into `the_executor`.

        Parameters
        ----------
        fn : Callable
            The global executor.

        Returns
        -------
        Callable
            The global executor `fn`.

        Example
        -------
        ```
        @execute_tests_like_this
        async def executor(chk_fn):
            return await chk_fn(args, to, be, passed=into)
        ```
        """
        self.the_executor = fn
        return fn

    def how_to_execute(self, test_name: str) -> typing.Callable:
        """
        Decorator for saving executor for a test.

        The executor will be saved into `executors`
        with the key being the test name.

        Parameters
        ----------
        test_name : str
            the name of the test.

        Returns
        -------
        decorator(fn: typing.Callable) -> typing.Callable
            A function (decorator) that saves the executor.

        Example
        -------
        ```
        @how_to_execute("my test")
        @how_to_execute("another test, put name here")
        async def special_test_executor(chk_fn):
            return await chk_fn(args, to, pass=into)
        ```
        """

        def decorator(fn: typing.Callable) -> typing.Callable:
            self.tests[test_name].executor = fn
            return fn

        return decorator

    def make_sure(self, fn: typing.Callable):
        """
        Checks for a call of `fn`.

        Parameters
        ----------
        fn : typing.Callable
            The function to be checked on

        Returns
        -------
        MakeSure
            What do you want to make sure?
        """
        return MakeSure(fn, self)

    def add_test(self, name: str):
        """Adds a test to the system.

        Parameters
        ----------
        name : str
            The name of the test.

        Returns
        -------
        AddTest
            A class that contains the decorators.

        Examples
        --------
        ```
        @sys.add_test("test name here")
        async def my_test():
            sys.make_sure(my_own_Callable).returned(1)
        @sys.add_test("test name here again").for_fn(my_own_Callable)
        async def my_test():
            sys.make_sure(my_own_Callable).returned(1)
        ```
        """

        class AddTest:
            @staticmethod
            def for_fn(fn: typing.Callable):
                def decorate(test: typing.Callable):
                    self.tests[name] = Test(test, fn, self.the_executor)
                    return fn

                return decorate

            @staticmethod
            def __call__(test: typing.Callable):
                self.tests[name] = Test(test, None, self.the_executor)
                return test

        return AddTest

    def inject(self, fn: typing.Callable):
        """
        Decorator that enables unit-testing on `fn`

        This allows listening of calls of the fn.
        Records can be found on `self._current_res`.

        Parameters
        ----------
        fn : Callable
            The function to be decorated aka. injected.

        Examples
        --------
        ```
        spy_on_this_fn_pls = sys.inject(spy_on_this_fn_pls)

        @sys.inject
        async def just_spy_on_this_coro():
            return just(something)
        ```
        """

        async def decorated(args, kwargs):
            args, kwargs = tidy_fn_call(fn, args, kwargs)
            if asyncio.iscoroutinefunction(fn):
                ret = await fn(*args, **kwargs)
            else:
                ret = fn(*args, **kwargs)
            self._current_res.append(Call(fn.__name__, args, kwargs, ret))
            return ret

        if asyncio.iscoroutinefunction(fn):
            logger.debug(f"INJECT coro {fn.__name__}")

            # prevents properties being overwritten,
            # like fn.__name__ and fn.__annotations__
            @functools.wraps(fn)
            async def wrap(*args, **kwargs):
                args, kwargs = tidy_fn_call(fn, args, kwargs)
                ret = await fn(*args, **kwargs)
                self._current_res.append(Call(fn.__name__, args, kwargs, ret))
                return ret

            return wrap
        else:
            logger.debug(f"INJECT func {fn.__name__}")

            @functools.wraps(fn)
            def wrap(*args, **kwargs):
                args, kwargs = tidy_fn_call(fn, args, kwargs)
                ret = fn(*args, **kwargs)
                self._current_res.append(Call(fn.__name__, args, kwargs, ret))
                return ret

            return wrap

    def override(self, target: typing.Callable):
        """
        Override the return value of function `target`

        Parameters
        ----------
        target : typing.Callable
            The specified function as a target

        Returns
        -------
        Override
            How do you want to override?

        Examples
        --------
        ```
        my_fn = override(my_fn).setReturn(0)
        ```
        """
        global t
        t = target

        class Override:
            @staticmethod
            def setReturn(val: typing.Any):
                """
                Set return value of `target`.

                Parameters
                ----------
                val : Any
                    The value to be returned.

                Returns
                -------
                Callable
                    The replaced `target`.

                Examples
                --------
                ```
                override(my_fn).setReturn(1)
                ```
                """
                global t
                target = t

                if asyncio.iscoroutinefunction(target):

                    @functools.wraps(target)
                    async def replacement(*_, **__):
                        return val

                    target = replacement
                else:

                    @functools.wraps(target)
                    def replacement(*_, **__):
                        return val

                    target = replacement

                target = replacement
                return target

            @staticmethod
            def setReturnAsResultOf(fn: typing.Callable):
                """
                Set the return value of the function as the return of `fn`.

                This is roughly equivalent to `target = fn`.
                `fn` will only be ran at runtime, not when you call this.

                Parameters
                ----------
                fn : Callable
                    Replace `target` to be `fn`.

                Examples
                --------
                ```
                override(target).setReturnAsResultOf(another_fn)

                @override(target).setReturnAsResultOf
                async def another_coro():
                    return 1234
                ```
                """
                global t
                target = t
                if asyncio.iscoroutinefunction(target):

                    @functools.wraps(target)
                    async def replacement(*_, **__):
                        if asyncio.iscoroutinefunction(fn):
                            return await fn()
                        return fn()

                    target = replacement
                else:

                    @functools.wraps(target)
                    def replacement(*_, **__):
                        if asyncio.iscoroutinefunction(fn):
                            return asyncio.run_coroutine_threadsafe(fn())
                        return fn()

                    target = replacement

                return target

            @staticmethod
            def makeItDoNothing():
                """
                Set `target` to do nothing.

                Example
                -------
                ```
                sys.override(target).makeItDoNothing()
                ```
                """
                global t
                target = t
                if asyncio.iscoroutinefunction(target):

                    @functools.wraps(target)
                    async def doNothing(*_, **__):
                        pass

                    target = doNothing
                else:

                    @functools.wraps(target)
                    def doNothing(*_, **__):
                        pass

                    target = doNothing

                target = doNothing
                return target

        return Override

    async def _test_out(self, name: str = None):
        """
        Parameters
        ----------
        name : str, optional
            the name of the test, by default None
        """
        if not name:  # huputs: breakpoint()
            for testname, test in self.tests.items():
                await test.executor(test.chk_fn)
            return
        test = self.tests[name]
        await test.executor(test.chk_fn)

    def do_this(self):
        asyncio.run(self._test_out())


class MakeSure:
    """
    Checks for a call of `fn`.

    Attributes
    ----------
    sys: TestThingsOut
        The unit test system
    fn: typing.Callable
        The function to be checked on

    Methods
    -------
    ran()
        Check if the function ever ran.
    ran_with_exactly(*args, **kwargs)
        Check if the function ran with the given arguments.
    ran_with_exactly_dictly(*args, **kwargs)
        Check if the function ran with the given arguments.
    ran_with_loosely(*args, **kwargs)
        Check if the function ran containing the given arguments.
    ran_with_loosely_dictly(*args, **kwargs)
        Check if the function ran containing the given arguments.
    ret(value: typing.Any)
        Check the return value.
    ret_dictly(value: dict)
        Check the return value.
    """

    sys: TestThingsOut
    fn: typing.Callable

    def __init__(self, function, sys):
        self.fn = function
        self.sys = sys

    def ran(self):
        """
        Check if the function ever ran.

        Raises
        ------
        TestError
            The function never ran.
        """
        try:
            assert any(
                [
                    call.name == self.fn.__name__
                    for call in self.sys._current_res
                ]
            ), f"Can't find '{self.fn.__name__}' in call records."
        except AssertionError as err:
            raise TestError(
                f"Expected '{self.fn.__name__}' to be ran."
            ) from err

    def ran_with_exactly(self, *args, **kwargs):
        """
        Check if the function ran with the given arguments.

        *args: positional arguments
        **kwargs: keyword arguments

        Raises
        ------
        TestError
            The function never ran with the specified arguments.
        """
        self.ran()  # make sure I ran
        stack = []  # args and kws that doesn't match
        ok = False
        args, kwargs = tidy_fn_call(self.fn, args, kwargs)
        for call in self.sys._current_res:
            if call.name != self.fn.__name__:
                continue
            if args == call.args and kwargs == call.kws:
                ok = True
                break
            stack.append((call.args, call.kws))
        if not ok:
            expected = visualise(*args, **kwargs)
            d = f"Expected:\t{self.fn.__name__}({expected})\n"  # description
            for i, (pos, kws) in enumerate(stack):
                d += (
                    f"Call #{i+1}:\t{self.fn.__name__}"
                    f"({diff(expected, visualise(*pos, **kws))})\n"
                )
            raise TestError(
                f"Expected '{self.fn.__name__}' to run with "
                "specified args or kwargs.\n" + d
            )

    def ran_with_exactly_dictly(self, *args, **kwargs):
        """
        Check if the function ran with the given arguments.

        WARN: You definitely DON'T want to use this. You have to match the
        WARN: magic properties (such as `__class__`, `__setattr__`, `__hash__`)
        WARN: in the dictionary. You probably fancy `ran_with_loosely_dictly`.

        *args: positional arguments
        **kwargs: keyword arguments

        Raises
        ------
        TestError
            The function never ran with the specified arguments.

        Examples
        --------
        ```
        class Something:
            def __init__(self, i):
                self.i = i

        fn(sth=Something(1))

        sys.make_sure(fn).ran_with_exactly_dictly(
            sth={'__class__': Something, 'i': 1, ...}
        )
        # yeah ... fill that in, I won't. Warned.
        ```
        """
        self.ran()
        stack = []
        ok = False
        args, kwargs = tidy_fn_call(self.fn, args, kwargs)
        for call in self.sys._current_res:
            if call.name != self.fn.__name__:
                continue
            callargs = [to_dict(a) for a in call.args]
            callkws = {k: to_dict(v) for k, v in call.kws.items()}
            if args == callargs and kwargs == callkws:
                ok = True
                break
            stack.append((callargs, callkws))
        if not ok:
            expected = visualise(*args, **kwargs)
            d = f"Expected:\t{expected}\n"  # description
            for i, (pos, kws) in enumerate(stack):
                d += f"Call #{i}:\t{diff(expected, visualise(*pos, **kws))}\n"
            raise TestError(
                f"Expected '{self.fn.__name__}' to run with "
                "specified args or kwargs.\n" + d
            )

    def ran_with_loosely(self, *args, **kwargs):
        """
        Check if the function ran containing the given arguments.

        *args: positional arguments
        **kwargs: keyword arguments

        Raises
        ------
        TestError
            The function never ran containing the specified arguments.

        Examples
        --------
        ```
        class Something:
            def __init__(self, i):
                self.i = i

        fn('I', 'F', 'D', sth=Something(1), another=2, a='boi')

        sys.make_sure(fn).ran_with_loosely('D', 'I', a='boi')
        ```
        """
        ok = False
        callargs: list
        callkws: dict
        desc: str = ""
        args, kwargs = tidy_fn_call(self.fn, args, kwargs)
        for call in self.sys._current_res:  # $ calliter
            if call.name != self.fn.__name__:
                continue  # $ calliter
            callargs = call.args
            for arg in args:  # * argiter
                if arg not in callargs:
                    desc += "Positional arguments: " + args
                    desc += "But it ran with:      " + callargs
                    break  # * argiter
            callkws = call.kws
            for key, val in kwargs.items():  # & kwiter
                if key not in callkws or callkws[key] != val:
                    desc += "Keyword arguments: " + kwargs
                    desc += "But it ran with:   " + callkws
                    break  # & kwiter
            if desc:
                continue  # $ calliter
            ok = True
            break  # $ calliter
        if not ok:
            desc: str = ""
            if callargs != args:
                desc += "Positional arguments: " + args
                desc += "But it ran with:      " + callargs
            if callkws != kwargs:
                desc += "Keyword arguments: " + kwargs
                desc += "But it ran with:   " + callkws
            raise TestError(
                f"Expected '{self.fn.__name__}' to run containing "
                "specified args or kwargs.\n" + desc
            )

    def ran_with_loosely_dictly(self, *args, **kwargs):
        """
        Check if the function ran containing the given arguments.

        *args: positional arguments
        **kwargs: keyword arguments

        Raises
        ------
        TestError
            The function never ran containing the specified arguments.

        Examples
        --------
        ```
        class Something:
            def __init__(self, i):
                self.i = i

        fn('I', 'F', 'D', sth=Something(1), another=2, a='boi')

        sys.make_sure(fn).ran_with_loosely_dictly(
            'D', 'I', sth={'__class__': Something, 'i': 1}
        )
        ```
        """
        ok = False
        callargs: list
        callkws: dict
        desc: str = ""
        args, kwargs = tidy_fn_call(self.fn, args, kwargs)
        for call in self.sys._current_res:  # $ calliter
            if call.name != self.fn.__name__:
                continue  # $ calliter
            callargs = [
                x
                if isinstance(x, (int, float, str, list, dict))
                else to_dict(x)
                for x in call.args
            ]
            for arg in args:  # * argiter
                if arg not in callargs:
                    desc += f"Positional arguments: {args}"
                    desc += f"But it ran with:      {callargs}"
                    break  # * argiter
            callkws = {k: to_dict(v) for k, v in call.kws.items()}
            for key, val in kwargs.items():  # & kwiter
                if key not in callkws:
                    desc += f"Keyword arguments: {kwargs}"
                    desc += f"But it ran with:   {callkws}"
                    break  # & kwiter
                if callkws[key] != val:
                    desc += f"Keyword arguments: {kwargs}"
                    desc += f"But it ran with:   {callkws}"
                    break  # & kwiter
            if desc:
                continue  # $ calliter
            ok = True
            break  # $ calliter
        if not ok:
            desc: str = ""
            if callargs != args:
                desc += f"Positional arguments: {args}"
                desc += f"But it ran with:      {callargs}"
            if callkws != kwargs:
                desc += f"Keyword arguments: {kwargs}"
                desc += f"But it ran with:   {callkws}"
            raise TestError(
                f"Expected '{self.fn.__name__}' to run containing "
                "specified args or kwargs.\n" + desc
            )

    def ret(self, value: typing.Any):
        """
        Check the return value.

        Parameters
        ----------
        value : typing.Any
            The value expected to be returned

        Raises
        ------
        TestError
            The return value does not match
        """
        self.ran()
        rets = []
        for call in self.sys._current_res:
            if call.name != self.fn.__name__:
                continue
            if call.ret == value:
                return
            rets.append(call.ret)
        raise TestError(
            f"Expected '{self.fn.__name__}' to return: {value}\nbut got:\n"
            "\n".join(rets)
        )

    def ret_dictly(self, value: dict):
        """
        Check the return value.

        For more info on how dictly works, check out
        ran_with_exactly_dictly()
        ran_with_loosely_dictly()

        Parameters
        ----------
        value : typing.Any
            The value expected to be returned

        Raises
        ------
        TestError
            The return value does not match
        """
        self.ran()
        rets = []
        for call in self.sys._current_res:
            if call.name != self.fn.__name__:
                continue
            if to_dict(call.ret) == value:
                return
            rets.append(call.ret)
        raise TestError(
            f"Expected '{self.fn.__name__}' to return: {value}\nbut got:\n"
            "\n".join(rets)
        )

    returned: ret
    returned_dictly: ret_dictly
