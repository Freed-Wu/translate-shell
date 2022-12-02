"""Fake logging."""
from logging import Handler


class RichHandler(Handler):
    """RichHandler."""

    def __init__(self, **kwargs: bool) -> None:
        """__init__.

        :param kwargs:
        :type kwargs: bool
        :rtype: None
        """
        super().__init__()

    def emit(self, record: str) -> str:
        """emit.

        :param record:
        :type record: str
        :rtype: str
        """
        return record
