"""Online Translator
====================
"""
import logging
from contextlib import suppress
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .. import Translator

logger = logging.getLogger(__name__)


@dataclass
class OnlineTranslator(Translator):
    """OnlineTranslator. All other online translators must be its subclass."""

    name: str
    timeout: int = 5

    def http_get(
        self, url: str, data: Any = None, header: dict[str, str] | None = None
    ) -> str:
        """Http get.

        :param url:
        :type url: str
        :param data:
        :type data: Any
        :param header:
        :type header: dict[str, str] | None
        :rtype: str
        """
        if header is None:
            header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                " AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/75.0.3770.100 Safari/537.36"
            }

        if data:
            query_string = urlencode(data)
            url = url + "?" + query_string

        with suppress(HTTPError, URLError):
            with urlopen(
                Request(url, None, header), timeout=self.timeout
            ) as r:  # skipcq: BAN-B310
                charset = r.headers.get_param("charset") or "utf-8"

                r = r.read().decode(charset)
                return r

        logger.warning(
            "Translator %s timed out, please check your network",
            self.name,
        )
        return ""

    @staticmethod
    def md5sum(text: str | bytes) -> str:
        """Md5sum.

        :param text:
        :type text: str | bytes
        :rtype: str
        """
        import hashlib

        m = hashlib.md5()  # nosec B324
        if isinstance(text, str):
            text = text.encode("utf-8")
        m.update(text)
        return m.hexdigest()

    @staticmethod
    def html_unescape(text: str) -> str:
        """Html unescape.

        :param text:
        :type text: str
        :rtype: str
        """
        import html

        return html.unescape(text)
