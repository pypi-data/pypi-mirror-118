"""HTML attributes dictionary.
"""
from __future__ import annotations

from .dict import MutableDict


class HTMLAttributes(MutableDict):
    """HTML attributes dictionary.

    Subclasses :class:`MutableDict`.

    This class functions like a dictionary, mapping HTML attribute names to values.
    """

    def to_html(self) -> str:
        """Convert the HTML attributes dictionary to an HTML string.

        Returns:
            str: HTML attributes.
        """

        def format_item(key, value):
            if value is True:
                return key

            if isinstance(value, (list, tuple)):
                value = " ".join(value)
            elif isinstance(value, dict):
                value = " ".join(f"{key}:{item};" for key, item in value.items())
            return f'{key}="{value}"'

        return " ".join(
            format_item(key, value)
            for key, value in self.get_object().items()
            if value not in (None, False, "")
        )
