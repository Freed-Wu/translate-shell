r"""Server
==========
"""
import re
from argparse import Namespace
from typing import Any, Tuple

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
            word = self._cursor_word(
                params.text_document.uri, params.position, True
            )
            if not word:
                return None
            self.args.text = word[0]
            # ignore processed text
            doc = get_processed_result_text(self.args)[0]
            if not doc:
                return None
            return Hover(
                contents=MarkupContent(kind=MarkupKind.PlainText, value=doc),
                range=word[1],
            )

        @self.feature(TEXT_DOCUMENT_COMPLETION)
        def completions(params: CompletionParams) -> CompletionList:
            r"""Completion history words.

            :param params:
            :type params: CompletionParams
            :rtype: CompletionList
            """
            word = self._cursor_word(
                params.text_document.uri, params.position, False
            )
            token = "" if word is None else word[0]
            items = [
                CompletionItem(
                    label=x,
                    kind=CompletionItemKind.Constant,
                    insert_text=x,
                )
                for x in HISTORY_FILE.read_text().splitlines()
                if x.startswith(token)
            ]
            return CompletionList(is_incomplete=False, items=items)

    def _cursor_line(self, uri: str, position: Position) -> str:
        r"""Cursor line.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :rtype: str
        """
        doc = self.workspace.get_document(uri)
        content = doc.source
        line = content.split("\n")[position.line]
        return str(line)

    def _cursor_word(
        self, uri: str, position: Position, include_all: bool = True
    ) -> Tuple[str, Range] | None:
        r"""Cursor word.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :param include_all:
        :type include_all: bool
        :rtype: Tuple[str, Range] | None
        """
        line = self._cursor_line(uri, position)
        cursor = position.character
        for m in re.finditer(r"\w+", line):
            end = m.end() if include_all else cursor
            if m.start() <= cursor <= m.end():
                word = (
                    line[m.start() : end],
                    Range(
                        start=Position(
                            line=position.line, character=m.start()
                        ),
                        end=Position(line=position.line, character=end),
                    ),
                )
                return word
        return None


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    TranslateShellLanguageServer(args, APPNAME, __version__).start_io()
