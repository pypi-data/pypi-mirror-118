"""
Utilities functions are here.

Functions
---------
tidy_fn_call(fn: typing.Callable, args: typing.Iterable, kwargs: dict)
    Put args to kwargs if they matches.
visualise(*args, **kwargs) -> str
    Return the visualisation of the calling
diff(s1: str, s2: str, *, RED=..., GREEN=..., RESET=...) -> str
    Colourise the string according to the differences between them.
to_dict(obj: typing.Any) -> dict
    Returns a dict containing the attributes of the object.
empty(cls)
    Make `cls`'s __init__ empty.
"""
import inspect
import typing

from colorama import Fore
from difflib import ndiff


def tidy_fn_call(fn: typing.Callable, args: typing.Iterable, kwargs: dict):
    """
    Put args to kwargs if they matches.

    This works like a function call parser.

    Parameters
    ----------
    fn : typing.Callable
        The function to be called (it won't be called).
    args : typing.Iterable
        The positional arguments.
    kwargs : dict
        The keyword arguments.

    Returns
    -------
    tuple
        args, kwargs
    """
    # we have to assign the stuff in `args` to `kwargs`
    args = list(args)
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if not any(args):
            break  # no more pos args to process
        if name in kwargs:
            continue  # already specified in kws
        # confirmed
        kwargs[name] = args.pop()
    # 1. no one wants None stuff
    # 2. cvt obj to dict
    kwargs = {
        k: v  # if isinstance(v, (str, list, dict)) else to_dict(v)
        for k, v in kwargs.items()
        if v
    }
    return args, kwargs


def visualise(*args, **kwargs) -> str:
    """
    Return the visualisation of the calling of function.

    Returns
    -------
    str
        The visualisation.

    Examples
    --------
    ```
    assert visualise(i=1, b="a string") == "i=1, b='a string'"
    ```
    """
    out = ", ".join(args)
    for k, v in kwargs.items():
        if out:
            out += ", "
        out += str(k) + "="
        if isinstance(v, str):
            out += f"'{v}'"
        else:
            out += str(v)
    return out


def diff(
    s1: str, s2: str, *, RED=Fore.RED, GREEN=Fore.GREEN, RESET=Fore.RESET
) -> str:
    """
    Colourise the string according to the differences between them.

    red:   should erase in `s1`
    green: should add into `s1`

    Parameters
    ----------
    s1 : str
        the main string
    s2 : str
        the string to be compared

    Returns
    -------
    str
        The colourised string.
    """
    out = ""
    for _, s in enumerate(ndiff(s1, s2)):
        if s[0] == " ":
            out += s[2]
        elif s[0] == "-":
            out += RED + s[2] + RESET
        elif s[0] == "+":
            out += GREEN + s[2] + RESET
    return str(out)


def to_dict(obj: typing.Any) -> dict:
    """
    Returns a dict containing the attributes of the object.

    Parameters
    ----------
    obj : typing.Any
        The object to convert from
    """
    if isinstance(obj, (int, float, str, list, dict)):
        return obj
    res = {}
    for name in dir(obj):
        attr = getattr(obj, name, None)
        if attr:  # make sure it is not blank
            res[name] = attr
    return res


def empty(cls):
    """
    Make `cls`'s __init__ empty.

    That means you don't need to specify any params to initialise `cls`.

    Returns
    -------
    cls
        a subclassed `cls`
    """

    class Whatever(cls):
        def __init__(self):
            pass

    Whatever.__name__ = cls.__name__

    return Whatever
