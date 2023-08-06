"""Utilities.
"""

from __future__ import annotations

from typing import Any, Callable, Tuple, Type, Union

from .mutable import Mutable


def is_instance(obj: Any, classes: Union[Type, Tuple]) -> bool:
    """Checks if the object is an instance of the given class.

    Args:
        obj (Any): Object to check.
        classes (Union[Type, Tuple]): Class or classes against which to check the
            object.

    Returns:
        bool: Indicates that the object was an instance of the class.
    """
    return isinstance(obj, classes) or (
        isinstance(obj, Mutable)
        and isinstance(obj._object, classes)  # pylint: disable=protected-access
    )


def is_subclass(cls: Type, classes: Union[Type, Tuple]) -> bool:
    """Checks if a target class is a subclass of the given classes.

    Args:
        cls (Type): Target class to check.
        classes (Union[Type, Tuple]): Class or classes against which to check the
            target subclass.

    Returns:
        bool: Indicates the target class is a subclass of the given classes.
    """
    return issubclass(cls, classes) or (
        isinstance(cls, Mutable)
        and issubclass(cls._object, classes)  # pylint: disable=protected-access
    )


class partial:  # pylint: disable=too-few-public-methods, invalid-name
    """Wrapper for callables stored in a mutable database column.

    This class's behavior mimics `functools.partial`.

    Args:
        func (Callable): Function to wrap.
        *args (Any): Arguments passed to the function when called.
        **kwargs (Any): Keyword arguments passed to the function when called.

    Attributes:
        func (Callable): Function to wrap.
        args (Tuple): Arguments passed to the function when called.
        kwargs (Dict): Keyword arguments passed to the function when called.
    """

    def __init__(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        self.func: Callable = func
        # args will be converted into a MutableTuple
        self.args = args
        # kwargs will be converted into a MutableDict
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        combined_kwargs = self.kwargs.get_object()  # pylint: disable=no-member
        combined_kwargs.update(kwargs)
        return self.func(
            *args,
            *self.args.get_object(),  # pylint: disable=no-member
            **combined_kwargs
        )
