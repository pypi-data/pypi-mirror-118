"""Mutable dictionary.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping

from .mutable import Mutable


@Mutable.register_class(dict)
class MutableDict(Mutable):
    """Mutable wrapper for dictionaries.

    Sublasses :class:`Mutable`.
    """

    @staticmethod
    def convert_object(obj: Mapping, root: Mutable) -> Dict[Any, Mutable]:
        """Convert an object into a mutable dictionary.

        Args:
            obj (Mapping): Object to convert.
            root (Mutable): Root mutable object.

        Returns:
            Dict[Any, Mutable]: Converted object.
        """
        if isinstance(obj, Mutable) and not isinstance(
            obj._object, dict  # pylint: disable=protected-access
        ):
            obj = obj.get_object()
        return (
            {}
            if obj is None
            else {key: Mutable(item, root) for key, item in dict(obj).items()}
        )

    def get_object(self) -> Dict[Any, Any]:
        """Get a shallow copy of the dictionary wrapped in the mutable object.

        Returns:
            Dict[Any, Any]: Shallow copy of the dictionary.
        """

        def get_object(item):
            if isinstance(item, Mutable):
                return item.get_object()
            return item

        return {key: get_object(item) for key, item in self._object.items()}

    def get_tracked_items(self) -> List[Mutable]:
        """Get the dictionary items whose mutations are being tracked.

        Returns:
            List[Mutable]: Tracked items.
        """
        return list(self._object.values())

    def clear(self):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.clear()

    def pop(self, key):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.pop(key)

    def popitem(self):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.popitem()

    def setdefault(self, key, value):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.setdefault(key, value)

    def update(self, iterable):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.update(iterable)
