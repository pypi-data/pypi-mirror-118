"""Mutable list.
"""

from __future__ import annotations

from typing import Any, Iterable, List

from .mutable import Mutable


@Mutable.register_class(list)
class MutableList(Mutable):
    """Mutable wrapper for lists.

    Subclasses :class:`Mutable`.
    """

    @staticmethod
    def convert_object(obj: Iterable, root: Mutable) -> List[Mutable]:
        """Convert an object into a mutable list.

        Args:
            obj (Iterable): Object to convert
            root (Mutable): Root mutable object.

        Returns:
            List[Mutable]: Converted object.
        """
        return [] if obj is None else [Mutable(item, root) for item in list(obj)]

    def get_object(self) -> List[Any]:
        """Get a shallow copy of the list wrapped in the mutable object.

        Returns:
            List[Any]: Shallow copy of the list.
        """
        return [item.get_object() for item in self._object]

    def get_tracked_items(self) -> List[Mutable]:
        """Get the list of items whose mutations are being tracked.

        Returns:
            List[Mutable]: Tracked items.
        """
        return list(self)

    def append(self, item):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.append(Mutable(item, self.root))

    def clear(self):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.clear()

    def extend(self, iterable):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.extend((Mutable(item, self.root) for item in iterable))

    def insert(self, index, item):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.insert(index, Mutable(item, self.root))

    def pop(self, index=-1):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.pop(index)

    def remove(self, item):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.remove(item)

    def reverse(self):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.reverse()

    def sort(self, reverse=False, key=None):  # pylint: disable=missing-docstring
        self._changed()
        return self._object.sort(reverse=reverse, key=key)

    def __iadd__(self, value):
        return super().__iadd__([Mutable(item, self.root) for item in value])
