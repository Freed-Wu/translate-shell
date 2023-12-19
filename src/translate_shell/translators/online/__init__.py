"""Online Translator
====================
"""
import logging
from dataclasses import dataclass

from aiohttp import ClientSession

from .. import Translator

logger = logging.getLogger(__name__)


@dataclass
class OnlineTranslator(Translator):
    """OnlineTranslator. All other online translators must be its subclass."""

    name: str
    timeout: int = 5

    async def http_get(
        self,
        url: str,
        session: ClientSession | None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> str:
        """Http get.

        :param url:
        :type url: str
        :param session:
        :type session: ClientSession | None
        :param params:
        :type params: dict[str, str] | None
        :param headers:
        :type headers: dict[str, str] | None
        :rtype: str
        """
        if session is None:
            _session = ClientSession()
        else:
            _session = session
        text = ""
        try:
            async with _session.get(
                url, params=params, headers=headers
            ) as resp:
                text = await resp.text()
        except Exception:
            logger.warning(
                "Translator %s timed out, please check your network", self.name
            )
        if session is None:
            await _session.close()
        return text

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
