"""Mutable tuple.
"""

from __future__ import annotations

from typing import Iterable, List, Tuple

from .mutable import Mutable


@Mutable.register_class(tuple)
class MutableTuple(Mutable):
    """Mutable wrapper for tuples.

    Subclasses :class:`Mutable`.
    """

    @staticmethod
    def convert_object(obj: Iterable, root: Mutable) -> Tuple:
        """Convert an object into a mutable tuple.

        Args:
            obj (Iterable): Object to convert.
            root (Mutable): Root mutable object.

        Returns:
            Tuple: Converted tuple.
        """
        return (
            tuple()
            if obj is None
            else tuple((Mutable(item, root) for item in tuple(obj)))
        )

    def get_object(self) -> Tuple:
        """Get a shallow copy of the tuple wrapped in the mutable object.

        Returns:
            Tuple: Shallow copy of the tuple.
        """
        return tuple((item.get_object() for item in self._object))

    def get_tracked_items(self) -> List[Mutable]:
        """Get the list of items whose mutations are being tracked.

        Returns:
            List[Mutable]: Tracked items.
        """
        return list(self)
