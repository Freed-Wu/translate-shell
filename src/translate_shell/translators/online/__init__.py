"""Online Translator
====================
"""
import logging
import socket
from copy import deepcopy
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .. import Translator

logger = logging.getLogger(__name__)


class OnlineTranslator(Translator):
    """OnlineTranslator. All other online translators must be its subclass."""

    def __init__(self, name: str) -> None:
        """Init.

        :param name:
        :type name: str
        :rtype: None
        """
        super().__init__(name)
        self._agent = (
            "Mozilla/5.0 (X11; Linux x86_64; rv:50.0) "
            "Gecko/20100101 Firefox/50.0"
        )
        self.timeout = 5

    def request(
        self,
        url: str,
        data: Any = None,
        post: bool = False,
        header: dict[str, str] | None = None,
    ) -> str:
        """Request.

        :param url:
        :type url: str
        :param data:
        :type data: Any
        :param post:
        :type post: bool
        :param header:
        :type header: dict[str, str] | None
        :rtype: str
        """
        if header:
            header = deepcopy(header)
        else:
            header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
            }

        if post:
            if data:
                data = urlencode(data).encode("utf-8")
        else:
            if data:
                query_string = urlencode(data)
                url = url + "?" + query_string
                data = None

        if url.lower().startswith("http"):
            req = Request(url, data, header)
        else:
            return ""

        try:
            with urlopen(req, timeout=self.timeout) as r:  # skipcq: BAN-B310
                charset = r.headers.get_param("charset") or "utf-8"

                r = r.read().decode(charset)
                return r

        except (HTTPError, socket.timeout):
            logger.warning(
                "Translator %s timed out, please check your network",
                self.name,
            )
            return ""

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
        return self.request(url, data, False, header)

    def http_post(
        self, url: str, data: Any = None, header: dict[str, str] | None = None
    ) -> str:
        """Http post.

        :param url:
        :type url: str
        :param data:
        :type data: Any
        :param header:
        :type header: dict[str, str] | None
        :rtype: str
        """
        return self.request(url, data, True, header)

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
