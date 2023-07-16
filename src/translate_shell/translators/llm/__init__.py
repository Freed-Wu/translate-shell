r"""LLM
=======
"""
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from jinja2 import Template

if TYPE_CHECKING:
    from llama_cpp import ChatCompletionMessage

from ...__main__ import LANGS
from ...external.platformdirs import AppDirs
from .. import TRANSLATION, Translator

TEMPLATES = []
for role in ["system", "user"]:
    template = AppDirs("translate-shell").user_config_path / (role + ".j2")
    if not template.exists():
        template = (
            Path(__file__).parent.parent.parent
            / "assets"
            / "jinja2"
            / (role + ".j2")
        )
    TEMPLATES += [{"role": role, "content": template.read_text()}]


class LLMTranslator(Translator):
    """Llmtranslator."""

    def __init__(self, name: str) -> None:
        """Init.

        :param name:
        :type name: str
        :rtype: None
        """
        super().__init__(name)

    def __call__(
        self, text: str, tl: str, sl: str, option: dict[str, Any]
    ) -> TRANSLATION | None:
        """Call.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :param option:
        :type option: dict[str, Any]
        :rtype: TRANSLATION | None
        """
        init_model = option.get("init_model", self.init_model)
        init_messages = option.get("init_messages", self.init_messages)
        init_kwargs = option.get("init_kwargs", self.init_kwargs)
        create_chat_completion = option.get(
            "create_chat_completion", self.create_chat_completion
        )
        init_result = option.get("init_result", self.init_result)

        model = init_model(option)
        messages = init_messages(tl, sl, text, option)
        kwargs = init_kwargs(option)

        completion = create_chat_completion(
            model=model, messages=messages, **kwargs
        )
        result = self.create_translation(text, tl, sl)
        result = init_result(completion, result)
        return result

    @staticmethod
    def init_model(option: dict) -> Any:
        """Init model.

        :param option:
        :type option: dict
        :rtype: Any
        """
        return option.get("model", "gpt-3.5-turbo")

    @staticmethod
    def init_messages(
        tl: str, sl: str, text: str, option: dict
    ) -> "list[ChatCompletionMessage]":
        """Init messages.

        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :param text:
        :type text: str
        :param option:
        :type option: dict
        :rtype: "ChatCompletionMessage"
        """
        templates = option.get("templates", TEMPLATES)
        messages = [
            {
                "role": template["role"],
                "content": Template(template["content"]).render(
                    tl=tl, sl=sl, text=text, langs=LANGS
                ),
            }
            for template in templates
        ]
        return messages  # type: ignore

    @staticmethod
    def init_kwargs(option: dict) -> dict:
        """Init kwargs.

        :param option:
        :type option: dict
        :rtype: dict
        """
        return {}

    @staticmethod
    def init_result(completion: Mapping, result: TRANSLATION) -> TRANSLATION:
        """Init result.

        :param completion:
        :type completion: Mapping
        :param result:
        :type result: TRANSLATION
        :rtype: TRANSLATION
        """
        result["paraphrase"] = completion["choices"][0]["message"]["content"]
        return result

    @staticmethod
    def create_chat_completion(
        model: Any, messages: list, **kwargs: Any
    ) -> Mapping:
        """Create chat completion.

        :param model:
        :type model: Any
        :param messages:
        :type messages: list
        :param kwargs:
        :type kwargs: Any
        :rtype: Mapping
        """
        if hasattr(model, "create_chat_completion"):
            return model.create_chat_completion(messages=messages, **kwargs)
        raise NotImplementedError
