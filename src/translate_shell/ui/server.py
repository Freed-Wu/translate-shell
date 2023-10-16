r"""Server
==========
"""
import re
from argparse import Namespace
from typing import Any

from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    Hover,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
    TextDocumentPositionParams,
)
from pygls.server import LanguageServer

from .. import APPNAME, HISTORY_FILE, __version__
from . import get_processed_result_text


class TranslateShellLanguageServer(LanguageServer):
    r"""Translate shell language server."""

    def __init__(self, translate_args: Namespace, *args: Any) -> None:
        """Init.

        :param self:
        :param translate_args:
        :type translate_args: Namespace
        :param args:
        :type args: Any
        :rtype: None
        """
        self.args = translate_args
        super().__init__(*args)

        @self.feature(TEXT_DOCUMENT_HOVER)
        def hover(params: TextDocumentPositionParams) -> Hover | None:
            r"""Hover the translated results.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: Hover | None
            """
            word, region = self._cursor_word(
                params.text_document.uri, params.position, True
            )
            self.args.text = word
            rst, _ = get_processed_result_text(self.args)
            if rst == "":
                return None
            return Hover(
                MarkupContent(MarkupKind.PlainText, rst),
                region,
            )

        @self.feature(TEXT_DOCUMENT_COMPLETION)
        def completions(params: CompletionParams) -> CompletionList:
            r"""Completion history words.

            :param params:
            :type params: CompletionParams
            :rtype: CompletionList
            """
            word, _ = self._cursor_word(
                params.text_document.uri, params.position, False
            )
            return CompletionList(
                False,
                [
                    CompletionItem(
                        x,
                        kind=CompletionItemKind.Constant,
                        insert_text=x,
                    )
                    for x in set(HISTORY_FILE.read_text().splitlines())
                    if x.startswith(word)
                ],
            )

    def _cursor_line(self, uri: str, position: Position) -> str:
        r"""Cursor line.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :rtype: str
        """
        document = self.workspace.get_document(uri)
        return document.source.splitlines()[position.line]

    def _cursor_word(
        self,
        uri: str,
        position: Position,
        include_all: bool = True,
        regex: str = r"\w+",
    ) -> tuple[str, Range]:
        """Cursor word.

        :param self:
        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :param include_all:
        :type include_all: bool
        :param regex:
        :type regex: str
        :rtype: tuple[str, Range]
        """
        line = self._cursor_line(uri, position)
        for m in re.finditer(regex, line):
            if m.start() <= position.character <= m.end():
                end = m.end() if include_all else position.character
                return (
                    line[m.start() : end],
                    Range(
                        Position(position.line, m.start()),
                        Position(position.line, end),
                    ),
                )
        return (
            "",
            Range(Position(position.line, 0), Position(position.line, 0)),
        )


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    TranslateShellLanguageServer(args, APPNAME, __version__).start_io()
