r"""LLaMa cpp
=============
"""
from typing import Any

from llama_cpp import Llama

from ...external.platformdirs import AppDirs
from . import LLMTranslator

# every time initing Llama costs about 1s
# cache to fasten
MODEL = Llama(
    str(AppDirs("translate-shell").user_data_path / "model.bin"), verbose=False
)


class LlamaTranslator(LLMTranslator):
    """Llamatranslator."""

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__("llama")

    @staticmethod
    def init_model(option: dict) -> Any:
        """Init model.

        :param option:
        :type option: dict
        :rtype: Any
        """
        return option.get("model", MODEL)
