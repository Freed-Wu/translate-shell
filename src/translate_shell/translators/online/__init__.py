"""Online Translator
====================
"""
import logging
import socket
from copy import deepcopy
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .. import Translator

logger = logging.getLogger(__name__)


class OnlineTranslator(Translator):
    """OnlineTranslator. All other online translators must be its subclass."""

    def __init__(self, name: str) -> None:
        """__init__.

        :param name:
        :type name: str
        :rtype: None
        """
        super().__init__(name)
        self._agent = (
            "Mozilla/5.0 (X11; Linux x86_64; rv:50.0) "
            "Gecko/20100101 Firefox/50.0"
        )

    def request(
        self,
        url: str,
        data: Any = None,
        post: bool = False,
        header: dict[str, str] | None = None,
    ) -> str:
        """request.

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
            header = {}
            header[
                "User-Agent"
            ] = "Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"

        if post:
            if data:
                data = urlencode(data).encode("utf-8")
        else:
            if data:
                query_string = urlencode(data)
                url = url + "?" + query_string
                data = None

        req = Request(url, data, header)

        try:
            r = urlopen(req, timeout=5)
        except (URLError, HTTPError, socket.timeout):
            logger.warning(
                "Translator %s timed out, please check your network"
                % self._name
            )
            return ""

        charset = r.headers.get_param("charset") or "utf-8"

        r = r.read().decode(charset)
        return r

    def http_get(
        self, url: str, data: Any = None, header: dict[str, str] | None = None
    ) -> str:
        """http_get.

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
        """http_post.

        :param url:
        :type url: str
        :param data:
        :type data: Any
        :param header:
        :type header: dict[str, str] | None
        :rtype: str
        """
        return self.request(url, data, True, header)

    def md5sum(self, text: str | bytes) -> str:
        """md5sum.

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

    def html_unescape(self, text: str) -> str:
        """html_unescape.

        :param text:
        :type text: str
        :rtype: str
        """
        import html

        return html.unescape(text)
